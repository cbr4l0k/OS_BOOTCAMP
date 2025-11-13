"""
Retrieval Node

LangGraph node for retrieving information from multiple sources.
This node orchestrates all retrieval adapters to gather data
relevant to the current query or sub-task.
"""

import logging
from typing import Callable
from src.domain.models import AgentState, Query, RetrievedData
from src.adapters.retrieval.orchestrator import RetrievalOrchestrator
from src.domain.ports import RetrievalPort
from src.domain.models import SourceProvider

logger = logging.getLogger(__name__)


def retrieval_node(
    state: AgentState,
    orchestrator: RetrievalOrchestrator,
) -> AgentState:
    """
    LangGraph node for information retrieval.

    This node:
    1. Determines what to search for (current task or main query)
    2. Calls retrieval adapters via orchestrator
    3. Collects sources from all enabled providers
    4. Updates state with retrieved data

    Args:
        state: Current agent state
        orchestrator: Retrieval orchestrator with configured adapters

    Returns:
        Updated agent state with retrieved data
    """
    logger.info("Starting retrieval node")

    # Step 1: Determine which query to retrieve
    # In Pro Mode with tasks, use the current task
    # Otherwise, use the main query
    if state.tasks and state.current_task_index < len(state.tasks):
        current_query = state.tasks[state.current_task_index]
        logger.info(
            f"Using task query {state.current_task_index + 1}/{len(state.tasks)}: "
            f"{current_query.content[:50]}..."
        )
    else:
        current_query = state.query
        logger.info(f"Using main query: {current_query.content[:50]}...")

    # Step 2: Execute retrieval
    try:
        retrieved_data = orchestrator.retrieve(current_query)
        logger.info(f"Successfully retrieved {len(retrieved_data.sources)} sources")

        # Log provider breakdown
        provider_counts = {}
        for source in retrieved_data.sources:
            provider_counts[source.provider] = provider_counts.get(source.provider, 0) + 1
        logger.debug(f"Sources by provider: {provider_counts}")

    except Exception as e:
        logger.error(f"Error during retrieval: {e}", exc_info=True)
        # Return empty results on error rather than failing completely
        retrieved_data = RetrievedData(sources=[])
        provider_counts = {}

    # Step 3: Update state with results and metadata
    # Note: We don't increment task_index here - that's the loop controller's job
    updated_memory = {
        **state.memory,
        'last_retrieval_sources': len(retrieved_data.sources),
        'last_retrieval_providers': list(provider_counts.keys()),
        'last_retrieval_query': current_query.content,
    }

    # Return updated state using model_copy for immutability
    return state.model_copy(
        update={
            'retrieved': retrieved_data,
            'memory': updated_memory,
        }
    )


def create_retrieval_node(
    adapters: list[RetrievalPort],
    enabled_providers: list[SourceProvider] | None = None,
) -> Callable[[AgentState], AgentState]:
    """
    Factory function to create a configured retrieval node.

    This allows us to inject dependencies and configuration at graph build time.

    Args:
        adapters: List of retrieval adapter instances
        enabled_providers: List of providers to enable (None = enable all)

    Returns:
        A configured retrieval node function ready to use in LangGraph

    Example:
        from src.adapters.retrieval.serp_adapter import TavilySerpAdapter
        from src.app.config import config

        # Create adapters
        serp = TavilySerpAdapter(api_key=config.tavily_api_key)

        # Create node
        node = create_retrieval_node(
            adapters=[serp],
            enabled_providers=[SourceProvider.SERP]
        )

        # Use in LangGraph
        graph.add_node("retrieval", node)
    """
    # If no providers specified, enable all adapters
    if enabled_providers is None:
        enabled_providers = [adapter.provider for adapter in adapters]

    # Create orchestrator
    orchestrator = RetrievalOrchestrator(
        adapters=adapters,
        enabled=enabled_providers
    )

    logger.info(
        f"Created retrieval node with {len(adapters)} adapters, "
        f"enabled providers: {[p.value for p in enabled_providers]}"
    )

    # Return a closure that captures the orchestrator
    def configured_node(state: AgentState) -> AgentState:
        return retrieval_node(state, orchestrator)

    return configured_node
