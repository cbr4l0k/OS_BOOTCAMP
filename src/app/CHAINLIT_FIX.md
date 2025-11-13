# Chainlit + LangChain v1.x Compatibility Fix

## The Problem

Chainlit's `LangchainCallbackHandler()` doesn't work with LangChain v1.x because LangChain restructured its callback system. You'll get this error:

```python
ModuleNotFoundError: No module named 'langchain.callbacks'
```

**Reference**: [Chainlit Issue #2607](https://github.com/Chainlit/chainlit/issues/2607)

## The Solution

We've implemented a simple fix using LangChain v1.x's new `astream_events()` API instead of the deprecated callbacks.

### What Changed

#### ❌ Old Code (Broken with LangChain v1.x)
```python
@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")
    msg = cl.Message(content="")

    # This doesn't work with LangChain v1.x!
    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
```

#### ✅ New Code (Works with LangChain v1.x)
```python
@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")
    msg = cl.Message(content="")
    await msg.send()

    # Use astream_events instead!
    async for event in runnable.astream_events(
        {"question": message.content},
        version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content"):
                content = chunk.content
                if content:
                    await msg.stream_token(content)

    await msg.update()
```

## For Simple Chains (Current Setup)

Your current setup just uses a simple LLM chain:
```
prompt | model | parser
```

The fix in `main.py` is all you need. No additional configuration required!

## For Agents with Tools (Future Use)

When you add agents and tools to TeraFinder, you'll need to use the middleware tracer.

### Example: Agent with Tools

```python
from src.app.chainlit_middleware import ChainlitMiddlewareTracer
from langgraph.prebuilt import create_react_agent
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    # Set up your tools
    tools = [
        # your tools here
    ]

    # Create agent with middleware
    agent = create_react_agent(
        model=llm,
        tools=tools,
        middleware=[ChainlitMiddlewareTracer()],  # Add this!
    )

    cl.user_session.set("agent", agent)


@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")

    msg = cl.Message(content="")
    await msg.send()

    # Stream agent responses
    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": message.content}]},
        version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content"):
                content = chunk.content
                if content:
                    await msg.stream_token(content)

    await msg.update()
```

The middleware will automatically track tool calls as Chainlit Steps, giving you nice UI visualization!

## Benefits

✅ **Works with LangChain v1.x**: No more import errors
✅ **Real-time streaming**: Smooth token-by-token streaming
✅ **Tool visualization**: When you add tools, they'll appear as steps in the UI
✅ **Future-proof**: Uses the modern LangChain API

## Testing

Run your Chainlit app:
```bash
chainlit run src/app/main.py
```

You should see:
- Smooth streaming responses
- No callback-related errors
- Clean UI without errors

## Need Help?

If you encounter issues:
1. Check that you're using LangChain v1.x: `pip show langchain`
2. Make sure Chainlit is updated: `pip install -U chainlit`
3. Review the [GitHub issue](https://github.com/Chainlit/chainlit/issues/2607) for updates

---

**Summary**: The fix is already implemented in `main.py`. Just run your app and it'll work! The middleware file is ready for when you add agents/tools later.
