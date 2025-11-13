"""
Conversation Adapter

This adapter handles conversational interactions with the user.
Allows for query clarification, follow-up questions, and interactive refinement.

TO IMPLEMENT:
1. Use an LLM for natural conversation
2. Track conversation history
3. Clarify ambiguous queries
4. Handle follow-up questions
"""

from src.domain.ports import ConversationPort
from src.domain.models import AgentState


class ChatAgent(ConversationPort):
    """
    Handles conversational interaction with users.

    Example usage:
        agent = ChatAgent(llm_client=llm)
        state = AgentState(query=Query("..."))
        response = agent.chat("Can you explain more about X?", state)
    """

    def __init__(self, llm_client=None):
        """
        Initialize the Chat Agent.

        Args:
            llm_client: LLM client for generating responses
        """
        self.llm = llm_client

    def chat(self, message: str, context: AgentState) -> str:
        """
        Generate a conversational response.

        Args:
            message: User's message
            context: Current agent state with conversation history

        Returns:
            Agent's response as a string
        """
        # TODO: Implement conversational logic
        #
        # Steps:
        # 1. Get conversation history from context
        # 2. Understand user intent (clarification, follow-up, new query)
        # 3. Generate appropriate response using LLM
        # 4. Update conversation history
        # 5. Return response

        # Placeholder response
        response = f"I received your message: '{message}'. This is a placeholder response."

        # Example implementation:
        # # Build conversation history
        # conversation_history = "\n".join(context.conversation[-5:])  # Last 5 messages
        #
        # # Get current query context
        # current_query = context.query.content if context.query else "No active query"
        #
        # # Check if we have any results to reference
        # has_results = bool(context.answer and context.answer.conclusion)
        # results_summary = ""
        # if has_results:
        #     results_summary = f"\n\nCurrent findings: {context.answer.conclusion[:200]}..."
        #
        # # Build prompt for LLM
        # prompt = f"""
        # You are a helpful research assistant. You're having a conversation with a user
        # about their research query.
        #
        # Current Research Topic: {current_query}
        # {results_summary}
        #
        # Recent Conversation:
        # {conversation_history}
        #
        # User: {message}
        #
        # Respond naturally and helpfully. You can:
        # - Answer questions about the research
        # - Ask clarifying questions
        # - Suggest related topics
        # - Explain your research process
        #
        # Assistant:
        # """
        #
        # try:
        #     # Generate response
        #     # response = self.llm.complete(prompt, temperature=0.7)
        #
        #     # Update conversation history (done by caller typically)
        #     # context.conversation.append(f"User: {message}")
        #     # context.conversation.append(f"Assistant: {response}")
        #
        # except Exception as e:
        #     print(f"Error in chat agent: {e}")
        #     response = "I apologize, but I encountered an error. Could you rephrase your question?"

        return response


# HELPFUL RESOURCES:
# - LangChain conversation memory
# - Conversational AI patterns
# - OpenAI Chat Completion API
# - Chainlit for UI
#
# TIPS:
# - Keep conversation history to prevent context bloating
# - Use system messages to set assistant behavior
# - Detect intent: is user asking a new question or following up?
# - Reference previous messages naturally
# - Ask clarifying questions when query is ambiguous
# - Summarize long conversations to maintain context
# - Handle edge cases: off-topic questions, greetings, etc.
# - Use higher temperature (0.7-0.9) for more natural conversation
# - Lower temperature (0.3-0.5) for factual answers
# - Consider using function calling to trigger actions (new search, etc.)
# - Add personality but keep it professional
