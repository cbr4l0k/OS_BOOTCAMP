"""
Formatting Node

LangGraph node for formatting structured answers into markdown.
This node takes the synthesized answer and creates a user-friendly
markdown output with citations and metadata.
"""

import logging
from typing import Callable

from src.domain.models import AgentState
from src.adapters.formatting.markdown_formatter import MarkdownFormatter

logger = logging.getLogger(__name__)


def formatting_node(state: AgentState, formatter: MarkdownFormatter) -> AgentState:
    """
    LangGraph node for formatting the answer.

    This node:
    1. Takes the synthesized answer from state
    2. Formats it into markdown with citations
    3. Stores the formatted output in state memory

    Args:
        state: Current agent state
        formatter: MarkdownFormatter instance (injected via factory)

    Returns:
        Updated agent state with formatted output in memory
    """
    logger.info("Starting formatting...")

    # Check if we have an answer to format
    if not state.answer:
        logger.warning("No answer available for formatting, skipping")
        return state

    # Format the answer
    logger.info("Formatting answer into markdown...")
    formatted_output = formatter.format(state.answer)

    logger.info(
        f"Formatting complete. Output length: {len(formatted_output)} chars"
    )

    # Update state using model_copy for immutability
    return state.model_copy(
        update={
            'memory': {
                **state.memory,
                'formatted_output': formatted_output,
                'formatting_complete': True,
                'output_length': len(formatted_output)
            }
        }
    )


def create_formatting_node(
    include_metadata: bool = True
) -> Callable[[AgentState], AgentState]:
    """
    Factory function to create a configured formatting node.

    This allows us to configure the formatter at graph build time.

    Args:
        include_metadata: Whether to include metadata in formatted output

    Returns:
        A configured formatting node function ready to use in LangGraph

    Example:
        # Create node
        node = create_formatting_node(include_metadata=True)

        # Use in LangGraph
        graph.add_node("format", node)
    """
    # Create formatter with configuration
    formatter = MarkdownFormatter(include_metadata=include_metadata)

    logger.info(
        f"Created formatting node (include_metadata={include_metadata})"
    )

    # Return a closure that captures the formatter
    def configured_node(state: AgentState) -> AgentState:
        return formatting_node(state, formatter)

    return configured_node
