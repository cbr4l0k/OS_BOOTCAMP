"""
Task Decomposition Adapter

This adapter breaks complex queries into smaller sub-queries.
Enables systematic exploration of multi-faceted questions.

TO IMPLEMENT:
1. Use an LLM to analyze the query
2. Break it into logical sub-questions
3. Order sub-questions by dependency or priority
4. Return a list of Query objects
"""

from src.domain.ports import TaskDecompositionPort
from src.domain.models import Query


class Decomposer(TaskDecompositionPort):
    """
    Decomposes complex queries into sub-tasks.

    Example usage:
        decomposer = Decomposer(llm_client=llm)
        main_query = Query(content="How does climate change affect biodiversity?")
        sub_queries = decomposer.decompose(main_query)
    """

    def __init__(self, llm_client=None, max_subtasks: int = 5):
        """
        Initialize the Decomposer.

        Args:
            llm_client: LLM client for query analysis
            max_subtasks: Maximum number of sub-tasks to create
        """
        self.llm = llm_client
        self.max_subtasks = max_subtasks

    def decompose(self, query: Query) -> list[Query]:
        """
        Decompose a query into sub-queries.

        Args:
            query: The main query to decompose

        Returns:
            List of sub-queries
        """
        # TODO: Implement query decomposition logic
        #
        # Steps:
        # 1. Analyze the query for complexity
        # 2. Identify main topics or aspects
        # 3. Generate sub-questions that cover each aspect
        # 4. Order by logical flow or dependency
        # 5. Limit to max_subtasks
        # 6. Return as Query objects

        # Placeholder: return the original query as-is
        # return [query]

        # Example implementation:
        # # Check if query is complex enough to decompose
        # if len(query.content.split()) < 5:
        #     # Simple query, don't decompose
        #     return [query]
        #
        # # Use LLM to decompose
        # try:
        #     prompt = f"""
        #     Break down this complex question into {self.max_subtasks} or fewer sub-questions.
        #     Each sub-question should:
        #     - Address a specific aspect of the main question
        #     - Be answerable independently
        #     - Build toward answering the main question
        #
        #     Main Question: {query.content}
        #
        #     Return ONLY the sub-questions, one per line, numbered:
        #     1. [sub-question]
        #     2. [sub-question]
        #     ...
        #
        #     If the question is simple and doesn't need decomposition, return just:
        #     SIMPLE
        #     """
        #
        #     # response = self.llm.complete(prompt, temperature=0.3)
        #
        #     # # Parse response
        #     # if "SIMPLE" in response:
        #     #     return [query]
        #     #
        #     # # Extract numbered questions
        #     # import re
        #     # lines = response.strip().split('\n')
        #     # sub_queries = []
        #     #
        #     # for line in lines:
        #     #     # Match patterns like "1. Question?" or "1) Question?"
        #     #     match = re.match(r'^\d+[\.)]\s*(.+)$', line.strip())
        #     #     if match:
        #     #         sub_question = match.group(1).strip()
        #     #         sub_queries.append(Query(content=sub_question))
        #     #
        #     # # Limit to max_subtasks
        #     # sub_queries = sub_queries[:self.max_subtasks]
        #     #
        #     # # If decomposition failed, return original
        #     # if not sub_queries:
        #     #     return [query]
        #     #
        #     # return sub_queries
        #
        # except Exception as e:
        #     print(f"Error in query decomposition: {e}")
        #     # Fallback: return original query
        #     return [query]

        # Simple heuristic-based decomposition (no LLM):
        # You could detect question words and split accordingly
        # Example: "What is X and how does Y work?" -> ["What is X?", "How does Y work?"]

        return [query]  # Placeholder


# HELPFUL RESOURCES:
# - Question decomposition in NLP
# - LangChain query transformation
# - Multi-hop question answering research
#
# TIPS:
# - Look for conjunctions (and, or) and complex structures
# - Order sub-questions logically (definition before application)
# - Some questions need sequential answering (A before B)
# - Others can be answered in parallel
# - Tag sub-queries with metadata (topic, priority, dependencies)
# - Consider using few-shot examples in your prompt
# - For very complex queries, use hierarchical decomposition
# - Track which sub-queries have been answered
# - Combine answers from sub-queries into final answer
# - Don't over-decompose simple questions
