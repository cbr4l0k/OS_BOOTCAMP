"""
Verification Node

LangGraph node for verifying and validating retrieved data.
This node checks sources for consistency, reliability, and accuracy.
"""

import logging
from typing import Callable, Optional

from src.domain.models import AgentState
from src.adapters.verification.verifier import Verifier

logger = logging.getLogger(__name__)


def verification_node(state: AgentState, verifier: Verifier) -> AgentState:
    """
    LangGraph node for data verification.

    This node:
    1. Takes retrieved data from state
    2. Verifies facts across sources
    3. Assigns dynamic confidence scores
    4. Updates state with verified data

    Args:
        state: Current agent state
        verifier: Verifier instance (injected via factory)

    Returns:
        Updated agent state with verified data
    """
    logger.info("Starting verification...")

    # Check if we have retrieved data
    if not state.retrieved or not state.retrieved.sources:
        logger.warning("No retrieved data to verify, skipping")
        return state

    num_sources = len(state.retrieved.sources)
    logger.info(f"Verifying {num_sources} sources...")

    # Run verification
    verified_data = verifier.verify(state.retrieved)

    logger.info(
        f"Verification complete. Confidence: {verified_data.confidence:.2%}, "
        f"Diversity: {verified_data.diversity_score:.2%}, "
        f"Facts: {len(verified_data.facts)}"
    )

    # Update state using model_copy for immutability
    return state.model_copy(
        update={
            'verified': verified_data,
            'memory': {
                **state.memory,
                'verification_complete': True,
                'verification_confidence': verified_data.confidence,
                'diversity_score': verified_data.diversity_score,
                'num_verified_facts': len(verified_data.facts),
                'num_sources_verified': num_sources
            }
        }
    )


def create_verification_node(
    llm_client=None,
    min_sources_for_high_confidence: int = 5,
    use_llm_verification: bool = False
) -> Callable[[AgentState], AgentState]:
    """
    Factory function to create a configured verification node.

    This allows us to inject configuration at graph build time.

    Args:
        llm_client: Optional LLM client for advanced fact-checking
        min_sources_for_high_confidence: Minimum sources needed for high confidence
        use_llm_verification: Whether to use LLM for cross-source verification

    Returns:
        A configured verification node function ready to use in LangGraph

    Example:
        from langchain_openai import ChatOpenAI
        from src.app.config import config

        # Create LLM client (optional)
        llm = ChatOpenAI(
            api_key=config.openai_api_key,
            base_url=config.openai_api_base,
            model=config.model_name
        )

        # Create node
        node = create_verification_node(
            llm_client=llm,
            min_sources_for_high_confidence=5,
            use_llm_verification=False  # Enable when ready
        )

        # Use in LangGraph
        graph.add_node("verification", node)
    """
    # Create verifier with configuration
    verifier = Verifier(
        llm_client=llm_client,
        min_sources_for_high_confidence=min_sources_for_high_confidence,
        use_llm_verification=use_llm_verification
    )

    logger.info(
        f"Created verification node "
        f"(min_sources={min_sources_for_high_confidence}, "
        f"llm_verification={use_llm_verification})"
    )

    # Return a closure that captures the verifier
    def configured_node(state: AgentState) -> AgentState:
        return verification_node(state, verifier)

    return configured_node
