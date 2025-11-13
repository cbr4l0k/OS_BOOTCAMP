from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.callbacks import YourCallbackClass

from typing import cast

import chainlit as cl
import os


@cl.on_chat_start
async def on_chat_start():
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
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
