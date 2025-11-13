"""
Conversation Node

LangGraph node for handling conversational interactions.
This node manages the initial conversation with the user to clarify
and refine their query before proceeding with research.

TO IMPLEMENT:
1. Connect to the conversation adapter
2. Process user input
3. Update agent state with conversation history
4. Decide when to move to decomposition
"""

from src.domain.models import AgentState
from src.adapters.conversation.chat_agent import ChatAgent


def conversation_node(state: AgentState) -> AgentState:
    """
    LangGraph node for conversation handling.

    This node:
    1. Takes user input
    2. Engages in conversation to clarify the query
    3. Updates conversation history
    4. Determines when query is ready for processing

    Args:
        state: Current agent state

    Returns:
        Updated agent state
    """
    # TODO: Implement conversation node logic
    #
    # Steps:
    # 1. Initialize chat agent
    # 2. Process the latest message
    # 3. Add response to conversation history
    # 4. Determine if query is clear enough
    # 5. Update state and return

    # Placeholder: just pass through
    # return state

    # Example implementation:
    # # Initialize chat agent
    # chat_agent = ChatAgent(llm_client=None)  # TODO: inject LLM
    #
    # # Get the latest user message
    # if state.conversation:
    #     latest_message = state.conversation[-1]
    # else:
    #     # First interaction - use the query content
    #     latest_message = state.query.content
    #
    # # Generate response
    # response = chat_agent.chat(latest_message, state)
    #
    # # Update conversation history
    # new_conversation = state.conversation.copy()
    # new_conversation.append(f"User: {latest_message}")
    # new_conversation.append(f"Assistant: {response}")
    #
    # # Update state
    # return AgentState(
    #     query=state.query,
    #     conversation=new_conversation,
    #     tasks=state.tasks,
    #     current_task_index=state.current_task_index,
    #     retrieved=state.retrieved,
    #     verified=state.verified,
    #     answer=state.answer,
    #     iteration=state.iteration,
    #     memory=state.memory
    # )

    return state


# HELPFUL RESOURCES:
# - LangGraph documentation: https://langchain-ai.github.io/langgraph/
# - State management patterns
# - Conversation flow design
#
# TIPS:
# - This node typically runs at the beginning
# - May be skipped in Simple Mode
# - Should detect when user is ready to proceed
# - Can be re-entered for follow-up questions
# - Track conversation turns to prevent endless chat
# - Store important information in state.memory
# - Consider adding a "ready_to_proceed" flag in memory
