"""
Synthesis Node

LangGraph node for synthesizing verified data into answers.
This node combines information from multiple sources into
a coherent, well-reasoned response.
"""

import logging
from typing import Callable

from src.domain.models import AgentState, VerifiedData
from src.adapters.synthesis.synthesizer import Synthesizer

logger = logging.getLogger(__name__)


def synthesis_node(state: AgentState, synthesizer: Synthesizer) -> AgentState:
    """
    LangGraph node for answer synthesis.

    This node:
    1. Takes verified data from state (or retrieved data for Simple Mode)
    2. Synthesizes information into an answer
    3. Generates reasoning chain
    4. Updates state with structured answer

    Args:
        state: Current agent state
        synthesizer: Synthesizer instance (injected via factory)

    Returns:
        Updated agent state with synthesized answer
    """
    logger.info("Starting synthesis...")

    # Prefer verified data (Pro Mode), fall back to retrieved data (Simple Mode)
    if state.verified:
        # Pro Mode: Use real verified data from verification node
        logger.info(
            f"Pro Mode: Synthesizing from verified data "
            f"(confidence: {state.verified.confidence:.2%}, "
            f"diversity: {state.verified.diversity_score:.2%})"
        )
        data_to_synthesize = state.verified
    elif state.retrieved:
        # Simple Mode: Convert retrieved data to verified data (passthrough)
        # This maintains backwards compatibility with Simple Mode graphs
        logger.info("Simple Mode: Converting retrieved data to verified data (passthrough)")
        data_to_synthesize = VerifiedData(
            facts={"retrieved": state.retrieved.sources},
            confidence=0.7,  # Fixed confidence for Simple Mode
            diversity_score=0.5,
            corroboration={}
        )
    else:
        # No data to synthesize
        logger.warning("No data available for synthesis, skipping")
        return state

    # Run synthesis
    logger.info(f"Synthesizing answer from {len(data_to_synthesize.facts)} fact groups...")
    answer = synthesizer.synthesize(data_to_synthesize)

    # Increment iteration (we completed one loop)
    new_iteration = state.iteration + 1

    logger.info(
        f"Synthesis complete. Answer length: {len(answer.conclusion)} chars, "
        f"Confidence: {answer.metadata.get('confidence', 'N/A')}"
    )

    # Update state using model_copy for immutability
    return state.model_copy(
        update={
            'answer': answer,
            'iteration': new_iteration,
            'memory': {
                **state.memory,
                'synthesis_complete': True,
                'answer_length': len(answer.conclusion),
                'reasoning_steps': len(answer.reasoning.split('\n')) if answer.reasoning else 0,
                'synthesis_confidence': answer.metadata.get('confidence', 0.0)
            }
        }
    )


def create_synthesis_node(llm_client) -> Callable[[AgentState], AgentState]:
    """
    Factory function to create a configured synthesis node.

    This allows us to inject the LLM client at graph build time.

    Args:
        llm_client: LLM client for generating answers (e.g., ChatOpenAI)

    Returns:
        A configured synthesis node function ready to use in LangGraph

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
        node = create_synthesis_node(llm_client=llm)

        # Use in LangGraph
        graph.add_node("synthesis", node)
    """
    # Create synthesizer with LLM client
    synthesizer = Synthesizer(llm_client=llm_client)

    logger.info("Created synthesis node with configured LLM client")

    # Return a closure that captures the synthesizer
    def configured_node(state: AgentState) -> AgentState:
        return synthesis_node(state, synthesizer)

    return configured_node
