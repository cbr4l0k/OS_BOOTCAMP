"""
TeraFinder Chainlit Application

This is the main entry point for the Chainlit UI.
Uses LangChain v1.x compatible streaming (astream_events) instead of
deprecated callbacks.

For the callback compatibility issue, see:
https://github.com/Chainlit/chainlit/issues/2607
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from typing import cast
import chainlit as cl

from src.app.config import config



@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session with the LLM and prompt."""
    api_key = config.openai_api_key
    base_url = config.openai_api_base

    # The API uses standard Bearer token authentication
    # No custom headers needed - just pass the API key directly
    model = ChatOpenAI(
        streaming=config.streaming,
        model_name=config.model_name,
        openai_api_base=base_url,
        openai_api_key=api_key,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
            ),
            ("human", "{question}"),
        ]
    )

    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages using LangChain v1.x compatible streaming.

    This uses astream_events() instead of the deprecated callback handler.
    The callback handler (cl.LangchainCallbackHandler) doesn't work with
    LangChain v1.x due to API changes.
    """
    runnable = cast(Runnable, cl.user_session.get("runnable"))

    msg = cl.Message(content="")
    await msg.send()

    # Use astream_events for LangChain v1.x compatibility
    # This replaces the deprecated callbacks approach
    async for event in runnable.astream_events(
        {"question": message.content},
        version="v2"  # Use v2 events API
    ):
        # Stream tokens from the chat model
        if event["event"] == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content"):
                content = chunk.content
                if content:
                    await msg.stream_token(content)

    await msg.update()
