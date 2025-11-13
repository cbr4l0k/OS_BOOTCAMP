"""
TeraFinder Chainlit Application

This is the main entry point for the Chainlit UI.
Integrates the Simple Mode LangGraph pipeline for fast search and answer generation.
"""

import chainlit as cl
from langchain_openai import ChatOpenAI

from src.app.config import config
from src.agents.graph import create_simple_mode_graph, create_initial_state
from src.adapters.retrieval.serp_adapter import TavilySerpAdapter
from src.domain.models import SourceProvider


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session with the TeraFinder Simple Mode graph."""

    # Send welcome message
    await cl.Message(
        content=(
            "# 🔍 Welcome to TeraFinder!\n\n"
            "I'm your AI-powered research assistant. I can help you find and synthesize "
            "information from across the web.\n\n"
            "**Simple Mode** is active - I'll give you fast answers with citations.\n\n"
            "Ask me anything!"
        )
    ).send()

    # Initialize retrieval adapters
    serp_adapter = TavilySerpAdapter(api_key=config.tavily_api_key)

    # Initialize LLM client
    llm = ChatOpenAI(
        api_key=config.openai_api_key,
        base_url=config.openai_api_base,
        model=config.model_name,
        temperature=0.3,
        streaming=True  # Enable streaming for real-time updates
    )

    # Create Simple Mode graph
    graph = create_simple_mode_graph(
        retrieval_adapters=[serp_adapter],
        llm_client=llm,
        enabled_providers=[SourceProvider.SERP],
        include_metadata=True
    )

    # Store graph in session
    cl.user_session.set("graph", graph)


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages using the TeraFinder graph.

    Executes the Simple Mode pipeline:
    1. Retrieval - Search the web for relevant sources
    2. Synthesis - Generate answer with LLM
    3. Format - Create markdown output with citations
    """
    graph = cl.user_session.get("graph")

    # Create initial state from user query
    initial_state = create_initial_state(message.content)

    # Create message for streaming updates
    msg = cl.Message(content="")
    await msg.send()

    # Track which step we're on
    current_step = None

    try:
        # Show initial status
        await msg.stream_token("🔎 **Searching the web...**\n\n")

        # Execute graph and stream progress
        final_state = None
        async for chunk in graph.astream(initial_state, stream_mode="updates"):
            # chunk is a dict mapping node name -> state update
            for node_name, state_update in chunk.items():
                if node_name == "retrieval":
                    # Retrieval complete
                    num_sources = len(state_update.get("retrieved", {}).sources) if state_update.get("retrieved") else 0
                    await msg.stream_token(f"✅ Retrieved {num_sources} sources\n\n")
                    await msg.stream_token("🧠 **Analyzing sources and generating answer...**\n\n")
                elif node_name == "synthesis":
                    # Synthesis complete
                    await msg.stream_token("✅ Answer generated\n\n")
                    await msg.stream_token("📝 **Formatting response...**\n\n")
                elif node_name == "format":
                    # Save final state
                    final_state = state_update

        # Extract formatted output
        if final_state and "memory" in final_state:
            formatted_output = final_state["memory"].get("formatted_output")

            if formatted_output:
                # Clear intermediate content and show final formatted answer
                msg.content = formatted_output
                await msg.update()
            else:
                # Fallback if formatting failed
                msg.content = (
                    "❌ **Error**: Failed to generate formatted output.\n\n"
                    f"Answer: {final_state.get('answer', 'No answer generated')}"
                )
                await msg.update()
        else:
            msg.content = "❌ **Error**: Graph execution failed to produce output."
            await msg.update()

    except Exception as e:
        # Handle errors gracefully
        error_msg = (
            f"❌ **An error occurred**: {str(e)}\n\n"
            "Please try again or rephrase your question."
        )
        msg.content = error_msg
        await msg.update()

        # Log error for debugging
        import logging
        logging.error(f"Error processing message: {e}", exc_info=True)


# Optional: Add settings or commands
@cl.on_settings_update
async def on_settings_update(settings):
    """Handle settings updates (future: mode switching, provider selection)."""
    pass
