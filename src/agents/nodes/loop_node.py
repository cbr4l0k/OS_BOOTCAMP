"""
Loop Control Node

LangGraph node for controlling the reasoning loop.
This node decides whether to continue gathering information
or to stop and present the answer.

TO IMPLEMENT:
1. Use the loop controller adapter
2. Check stopping conditions
3. Return routing decision for LangGraph
"""

from src.domain.models import AgentState
from src.adapters.loop.loop_controller import LoopController


def loop_control_node(state: AgentState) -> AgentState:
    """
    LangGraph node for loop control.

    This node:
    1. Evaluates the current state
    2. Decides whether to continue or stop
    3. Sets a flag in memory for routing

    Args:
        state: Current agent state

    Returns:
        Updated agent state with loop control decision
    """
    # TODO: Implement loop control logic
    #
    # Steps:
    # 1. Initialize loop controller
    # 2. Check if we should continue
    # 3. Store decision in state.memory
    # 4. Return updated state

    # Placeholder: just pass through
    # return state

    # Example implementation:
    # # Initialize loop controller
    # controller = LoopController(
    #     max_iterations=5,
    #     min_confidence=0.7,
    #     min_sources=3
    # )
    #
    # # Check if we should continue
    # should_continue = controller.continue_loop(state)
    #
    # # Update state with decision
    # return AgentState(
    #     query=state.query,
    #     conversation=state.conversation,
    #     tasks=state.tasks,
    #     current_task_index=state.current_task_index,
    #     retrieved=state.retrieved,
    #     verified=state.verified,
    #     answer=state.answer,
    #     iteration=state.iteration,
    #     memory={
    #         **state.memory,
    #         'should_continue': should_continue,
    #         'stop_reason': _get_stop_reason(state, controller) if not should_continue else None
    #     }
    # )

    return state


def _get_stop_reason(state: AgentState, controller: LoopController) -> str:
    """Helper to determine why we're stopping."""
    if state.iteration >= controller.max_iterations:
        return "max_iterations_reached"
    if state.verified and state.verified.confidence >= controller.min_confidence:
        return "high_confidence"
    if state.answer and len(state.answer.conclusion) > 50:
        return "answer_complete"
    return "unknown"


def should_continue(state: AgentState) -> str:
    """
    Routing function for LangGraph conditional edges.

    This function is used by LangGraph to determine the next node.

    Args:
        state: Current agent state

    Returns:
        "continue" or "end" to route the graph
    """
    # Check the decision from loop_control_node
    should_loop = state.memory.get('should_continue', False)

    if should_loop:
        return "continue"  # Route back to retrieval
    else:
        return "end"  # Route to output/formatting


# HELPFUL RESOURCES:
# - LangGraph conditional edges
# - Control flow in agent systems
# - Decision making in AI loops
#
# TIPS:
# - This node is crucial for preventing infinite loops
# - Always have hard limits (max iterations, time)
# - Log the stop reason for debugging
# - Different queries may need different stopping criteria
# - Consider cost (API calls, time) in the decision
# - The should_continue function is used by LangGraph routing
# - May want different logic for Simple vs Pro mode
# - Track loop statistics for optimization
