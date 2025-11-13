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


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session with the LLM and prompt."""
    api_key = "e52291a2a8dfd704a8e89668f5472803"
    base_url = "https://foundation-models.api.cloud.ru/v1"

    model = ChatOpenAI(
        streaming=True,
        openai_api_key=api_key,
        openai_api_base=base_url,
        model_name="MiniMaxAI/MiniMax-M2"
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
