"""
Decomposition Node

LangGraph node for breaking down complex queries into sub-tasks.
This node analyzes the user's query and creates a list of
sub-queries that can be addressed systematically.
"""

import logging
from typing import Callable, Optional

from src.domain.models import AgentState
from src.adapters.tasks.decomposer import Decomposer

logger = logging.getLogger(__name__)


def decomposition_node(state: AgentState, decomposer: Decomposer) -> AgentState:
    """
    LangGraph node for query decomposition.

    This node:
    1. Analyzes the complexity of the query
    2. Breaks it into sub-tasks if needed
    3. Updates the task list in state
    4. Sets the task index to 0

    Args:
        state: Current agent state
        decomposer: Decomposer instance (injected via factory)

    Returns:
        Updated agent state with tasks
    """
    logger.info("Starting query decomposition...")

    # Decompose the query into sub-tasks
    logger.info(f"Main query: {state.query.content}")
    sub_queries = decomposer.decompose(state.query)

    num_tasks = len(sub_queries)
    was_decomposed = num_tasks > 1

    if was_decomposed:
        logger.info(
            f"Query decomposed into {num_tasks} sub-tasks:"
        )
        for i, task in enumerate(sub_queries, 1):
            logger.info(f"  Task {i}: {task.content[:80]}...")
    else:
        logger.info("Query is simple, no decomposition needed")

    # Update state using model_copy for immutability
    return state.model_copy(
        update={
            'tasks': sub_queries,
            'current_task_index': 0,  # Start at first task
            'memory': {
                **state.memory,
                'decomposed': was_decomposed,
                'num_tasks': num_tasks,
                'decomposition_complete': True
            }
        }
    )


def create_decomposition_node(
    llm_client=None,
    max_subtasks: int = 5,
    min_query_length: int = 10,
    use_llm: bool = True
) -> Callable[[AgentState], AgentState]:
    """
    Factory function to create a configured decomposition node.

    This allows us to inject the LLM client and configuration at graph build time.

    Args:
        llm_client: Optional LLM client for intelligent decomposition
        max_subtasks: Maximum number of sub-tasks to create (default: 5)
        min_query_length: Minimum words to consider for decomposition (default: 10)
        use_llm: Whether to use LLM for decomposition (default: True)

    Returns:
        A configured decomposition node function ready to use in LangGraph

    Example:
        from langchain_openai import ChatOpenAI
        from src.app.config import config

        # Create LLM client
        llm = ChatOpenAI(
            api_key=config.openai_api_key,
            base_url=config.openai_api_base,
            model=config.model_name,
            temperature=0.3
        )

        # Create node
        node = create_decomposition_node(
            llm_client=llm,
            max_subtasks=5,
            min_query_length=10,
            use_llm=True
        )

        # Use in LangGraph
        graph.add_node("decomposition", node)
    """
    # Create decomposer with configuration
    decomposer = Decomposer(
        llm_client=llm_client,
        max_subtasks=max_subtasks,
        min_query_length=min_query_length,
        use_llm=use_llm
    )

    logger.info(
        f"Created decomposition node "
        f"(max_subtasks={max_subtasks}, "
        f"min_query_length={min_query_length}, "
        f"use_llm={use_llm})"
    )

    # Return a closure that captures the decomposer
    def configured_node(state: AgentState) -> AgentState:
        return decomposition_node(state, decomposer)

    return configured_node
