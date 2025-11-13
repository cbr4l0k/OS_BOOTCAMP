#!/usr/bin/env python3
"""
Minimal test for the retrieval node implementation.
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.domain.models import AgentState, Query, SourceProvider
from src.agents.nodes.retrieval_node import create_retrieval_node
from src.adapters.retrieval.serp_adapter import TavilySerpAdapter
from src.app.config import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Test retrieval node with a single simple query."""
    logger.info("Testing retrieval node...")

    # Create initial state with a simple query
    state = AgentState(
        query=Query(content="What is Python?"),
        conversation=[],
        tasks=[],
        current_task_index=0,
        iteration=0,
        memory={}
    )

    # Create retrieval node with Tavily adapter
    tavily_adapter = TavilySerpAdapter(api_key=config.tavily_api_key)
    retrieval_node = create_retrieval_node(
        adapters=[tavily_adapter],
        enabled_providers=[SourceProvider.SERP]
    )

    # Run retrieval
    logger.info(f"Query: {state.query.content}")
    updated_state = retrieval_node(state)

    # Check results
    if updated_state.retrieved and len(updated_state.retrieved.sources) > 0:
        logger.info(f"✓ Success! Retrieved {len(updated_state.retrieved.sources)} sources")
        logger.info(f"✓ First source: {updated_state.retrieved.sources[0].title}")
        logger.info(f"✓ Memory: {updated_state.memory}")
    else:
        logger.error("✗ Failed: No sources retrieved")
        sys.exit(1)


if __name__ == "__main__":
    main()
