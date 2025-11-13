"""
TeraFinder Agent Graph

This module defines the LangGraph workflow for the TeraFinder search agent.
It orchestrates the flow between retrieval, synthesis, and formatting nodes.

Simple Mode: Fast search path (retrieval -> synthesis -> format)
Pro Mode: Full pipeline with verification and decomposition (coming in Phase 2)
"""

import logging
from typing import Any

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from src.domain.models import AgentState, Query, SourceProvider
from src.domain.ports import RetrievalPort
from src.agents.nodes.retrieval_node import create_retrieval_node
from src.agents.nodes.synthesis_node import create_synthesis_node
from src.agents.nodes.formatting_node import create_formatting_node

logger = logging.getLogger(__name__)


def create_simple_mode_graph(
    retrieval_adapters: list[RetrievalPort],
    llm_client: ChatOpenAI,
    enabled_providers: list[SourceProvider] | None = None,
    include_metadata: bool = True,
) -> StateGraph:
    """
    Create a Simple Mode graph for fast search and answer generation.

    Simple Mode Flow:
        START -> retrieval -> synthesis -> format -> END

    This bypasses decomposition and verification for speed,
    providing quick answers with citations.

    Args:
        retrieval_adapters: List of retrieval adapter instances
        llm_client: LLM client for synthesis (e.g., ChatOpenAI)
        enabled_providers: List of providers to enable (None = all)
        include_metadata: Whether to include metadata in output

    Returns:
        Compiled LangGraph ready to execute

    Example:
        from langchain_openai import ChatOpenAI
        from src.adapters.retrieval.serp_adapter import TavilySerpAdapter
        from src.app.config import config

        # Create adapters and LLM
        serp = TavilySerpAdapter(api_key=config.tavily_api_key)
        llm = ChatOpenAI(
            api_key=config.openai_api_key,
            base_url=config.openai_api_base,
            model=config.model_name
        )

        # Create graph
        graph = create_simple_mode_graph(
            retrieval_adapters=[serp],
            llm_client=llm
        )

        # Run graph
        result = graph.invoke({
            "query": Query(content="What is LangGraph?"),
            "conversation": [],
            "tasks": [],
            "current_task_index": 0,
            "retrieved": None,
            "verified": None,
            "answer": None,
            "iteration": 0,
            "memory": {}
        })

        # Get formatted output
        formatted_answer = result["memory"]["formatted_output"]
    """
    logger.info("Creating Simple Mode graph...")

    # Create configured nodes using factory functions
    retrieval_node = create_retrieval_node(
        adapters=retrieval_adapters,
        enabled_providers=enabled_providers
    )

    synthesis_node = create_synthesis_node(
        llm_client=llm_client
    )

    formatting_node = create_formatting_node(
        include_metadata=include_metadata
    )

    # Initialize the graph with AgentState
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("synthesis", synthesis_node)
    graph.add_node("format", formatting_node)

    # Define the flow: retrieval -> synthesis -> format -> END
    graph.set_entry_point("retrieval")
    graph.add_edge("retrieval", "synthesis")
    graph.add_edge("synthesis", "format")
    graph.add_edge("format", END)

    logger.info(
        "Simple Mode graph created with flow: "
        "retrieval -> synthesis -> format"
    )

    # Compile the graph
    compiled = graph.compile()

    logger.info("Graph compiled successfully")

    return compiled


def create_initial_state(query: str) -> dict[str, Any]:
    """
    Create an initial state for the graph.

    Args:
        query: User's search query

    Returns:
        Initial state dictionary ready for graph execution
    """
    return {
        "query": Query(content=query),
        "conversation": [],
        "tasks": [],
        "current_task_index": 0,
        "retrieved": None,
        "verified": None,
        "answer": None,
        "iteration": 0,
        "memory": {}
    }


# Example usage and testing
if __name__ == "__main__":
    """
    Example usage of the Simple Mode graph.

    To run this test:
    1. Ensure OPENAI_API_KEY and TAVILY_API_KEY are set in .env
    2. Run: python -m src.agents.graph
    """
    from src.adapters.retrieval.serp_adapter import TavilySerpAdapter
    from src.app.config import config

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("=" * 70)
    print("TeraFinder Simple Mode Graph - Test Run")
    print("=" * 70)

    # Create adapters
    print("\n[1/4] Initializing adapters...")
    serp_adapter = TavilySerpAdapter(api_key=config.tavily_api_key)

    # Create LLM client
    print("[2/4] Initializing LLM client...")
    llm = ChatOpenAI(
        api_key=config.openai_api_key,
        base_url=config.openai_api_base,
        model=config.model_name,
        temperature=0.3
    )

    # Create graph
    print("[3/4] Building Simple Mode graph...")
    simple_graph = create_simple_mode_graph(
        retrieval_adapters=[serp_adapter],
        llm_client=llm,
        enabled_providers=[SourceProvider.SERP]
    )

    # Run test query
    print("[4/4] Running test query...")
    test_query = "What is LangGraph and how does it work?"
    print(f"\nQuery: {test_query}\n")

    initial_state = create_initial_state(test_query)
    result = simple_graph.invoke(initial_state)

    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    if "formatted_output" in result["memory"]:
        print(result["memory"]["formatted_output"])
    else:
        print("Error: No formatted output generated")
        print(f"Final state: {result}")

    print("\n" + "=" * 70)
    print("METADATA")
    print("=" * 70)
    print(f"Iterations: {result['iteration']}")
    if result.get('retrieved'):
        print(f"Sources retrieved: {len(result['retrieved'].sources)}")
    print(f"Answer length: {result['memory'].get('answer_length', 0)} chars")
    print(f"Synthesis confidence: {result['memory'].get('synthesis_confidence', 'N/A')}")
    print("=" * 70)
