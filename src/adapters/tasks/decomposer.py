"""
Task Decomposition Adapter

This adapter breaks complex queries into smaller sub-queries.
Enables systematic exploration of multi-faceted questions.
"""

import logging
from typing import Optional
from pydantic import BaseModel, Field

from src.domain.ports import TaskDecompositionPort
from src.domain.models import Query
from src.domain.prompts import DECOMPOSITION_PROMPT

logger = logging.getLogger(__name__)


class DecompositionOutput(BaseModel):
    """Structured output from LLM for query decomposition."""
    is_complex: bool = Field(..., description="Whether the query is complex enough to decompose")
    reasoning: str = Field(..., description="Explanation of complexity assessment")
    sub_questions: list[str] = Field(default_factory=list, description="List of sub-questions if complex")


class Decomposer(TaskDecompositionPort):
    """
    Decomposes complex queries into sub-tasks.

    Uses an LLM to intelligently analyze query complexity and
    break down multi-faceted questions into focused sub-questions.

    Example usage:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        decomposer = Decomposer(llm_client=llm)

        main_query = Query(content="How does climate change affect biodiversity?")
        sub_queries = decomposer.decompose(main_query)
        # Returns: [Query("What is climate change?"),
        #           Query("What is biodiversity?"),
        #           Query("How does climate change impact ecosystems?")]
    """

    def __init__(
        self,
        llm_client=None,
        max_subtasks: int = 5,
        min_query_length: int = 10,
        use_llm: bool = True
    ):
        """
        Initialize the Decomposer.

        Args:
            llm_client: LLM client for query analysis (e.g., ChatOpenAI)
            max_subtasks: Maximum number of sub-tasks to create (default: 5)
            min_query_length: Minimum words to consider for decomposition (default: 10)
            use_llm: Whether to use LLM for decomposition (default: True)
        """
        self.llm = llm_client
        self.max_subtasks = max_subtasks
        self.min_query_length = min_query_length
        self.use_llm = use_llm and llm_client is not None

        if not self.use_llm:
            logger.warning(
                "Decomposer initialized without LLM - will use heuristic fallback"
            )

    def decompose(self, query: Query) -> list[Query]:
        """
        Decompose a query into sub-queries.

        Args:
            query: The main query to decompose

        Returns:
            List of sub-queries (or just the original query if simple)
        """
        logger.info(f"Analyzing query for decomposition: {query.content[:100]}...")

        # Quick heuristic: very short queries likely don't need decomposition
        word_count = len(query.content.split())
        if word_count < self.min_query_length:
            logger.info(
                f"Query is short ({word_count} words < {self.min_query_length}), "
                "skipping decomposition"
            )
            return [query]

        # Use LLM-based decomposition if available
        if self.use_llm:
            try:
                sub_queries = self._llm_decompose(query)
                if sub_queries and len(sub_queries) > 1:
                    logger.info(
                        f"Decomposed into {len(sub_queries)} sub-queries: "
                        f"{[sq.content[:50] + '...' for sq in sub_queries]}"
                    )
                    return sub_queries
                else:
                    logger.info("LLM determined query is simple, no decomposition needed")
                    return [query]
            except Exception as e:
                logger.error(f"Error in LLM decomposition: {e}", exc_info=True)
                logger.info("Falling back to heuristic decomposition")
                return self._heuristic_decompose(query)
        else:
            # Fallback to heuristic decomposition
            return self._heuristic_decompose(query)

    def _llm_decompose(self, query: Query) -> list[Query]:
        """
        Use LLM to decompose the query with structured output.

        Args:
            query: The main query to decompose

        Returns:
            List of sub-queries or [original query] if not complex
        """
        if not self.llm:
            raise ValueError("LLM client not available")

        # Format prompt
        prompt = DECOMPOSITION_PROMPT.format(
            query=query.content,
            max_subtasks=self.max_subtasks
        )

        logger.debug("Calling LLM for query decomposition...")

        # Create structured LLM with Pydantic output
        structured_llm = self.llm.with_structured_output(DecompositionOutput)

        # Call LLM
        result = structured_llm.invoke(prompt)

        logger.debug(
            f"LLM analysis: is_complex={result.is_complex}, "
            f"reasoning={result.reasoning}"
        )

        # Check if decomposition is needed
        if not result.is_complex or not result.sub_questions:
            logger.info(f"Query not complex: {result.reasoning}")
            return [query]

        # Convert sub-questions to Query objects
        sub_queries = [
            Query(content=sq.strip())
            for sq in result.sub_questions[:self.max_subtasks]
        ]

        # Validate we have valid sub-questions
        if not sub_queries or len(sub_queries) < 2:
            logger.warning(
                "LLM decomposition produced < 2 sub-questions, "
                "returning original query"
            )
            return [query]

        return sub_queries

    def _heuristic_decompose(self, query: Query) -> list[Query]:
        """
        Simple heuristic-based decomposition (fallback when no LLM).

        Looks for common patterns:
        - "X and Y" -> split on "and"
        - "X or Y" -> split on "or"
        - Multiple question marks -> split by question
        - "compare X and Y" -> ["What is X?", "What is Y?", "Comparison"]

        Args:
            query: The main query to decompose

        Returns:
            List of sub-queries
        """
        content = query.content.lower()

        # Check for comparison pattern
        if "compare" in content or "difference between" in content:
            logger.info("Detected comparison query, using comparison heuristic")
            return self._heuristic_comparison(query)

        # Check for multiple questions
        if content.count("?") > 1:
            logger.info("Detected multiple questions, splitting on '?'")
            parts = query.content.split("?")
            sub_queries = [
                Query(content=part.strip() + "?")
                for part in parts
                if part.strip()
            ]
            return sub_queries[:self.max_subtasks] if sub_queries else [query]

        # Check for conjunctions (and, or)
        if " and " in content or " or " in content:
            logger.info("Detected conjunction, attempting split")
            # This is very simplistic - just split on first "and"/"or"
            delimiter = " and " if " and " in content else " or "
            parts = query.content.split(delimiter, 1)

            if len(parts) == 2:
                sub_queries = [Query(content=part.strip()) for part in parts]
                return sub_queries

        # Default: no decomposition
        logger.info("No heuristic pattern matched, returning original query")
        return [query]

    def _heuristic_comparison(self, query: Query) -> list[Query]:
        """
        Heuristic for comparison questions.

        Pattern: "Compare X and Y" or "Difference between X and Y"
        -> ["What is X?", "What is Y?", "Compare X and Y"]

        Args:
            query: Comparison query

        Returns:
            List of sub-queries
        """
        content_lower = query.content.lower()

        # Extract entities being compared (very basic)
        # This is a simplified approach - LLM is much better at this
        if "compare" in content_lower:
            # Try to find what's after "compare"
            after_compare = query.content.split("compare", 1)[1] if "compare" in content_lower else ""
            if " and " in after_compare:
                parts = after_compare.split(" and ", 1)
                entity1 = parts[0].strip()
                entity2 = parts[1].strip().rstrip("?.")

                return [
                    Query(content=f"What is {entity1}?"),
                    Query(content=f"What is {entity2}?"),
                    Query(content=f"What are the key differences between {entity1} and {entity2}?")
                ][:self.max_subtasks]

        # Fallback
        return [query]
