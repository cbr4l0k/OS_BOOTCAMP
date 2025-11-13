"""
Decomposition Node

LangGraph node for breaking down complex queries into sub-tasks.
This node analyzes the user's query and creates a list of
sub-queries that can be addressed systematically.

TO IMPLEMENT:
1. Use the task decomposition adapter
2. Analyze query complexity
3. Create sub-tasks
4. Update agent state with task list
"""

from ...domain.models import AgentState
from ...adapters.tasks.decomposer import Decomposer


def decomposition_node(state: AgentState) -> AgentState:
    """
    LangGraph node for query decomposition.

    This node:
    1. Analyzes the complexity of the query
    2. Breaks it into sub-tasks if needed
    3. Updates the task list in state
    4. Sets the task index to 0

    Args:
        state: Current agent state

    Returns:
        Updated agent state with tasks
    """
    # TODO: Implement decomposition node logic
    #
    # Steps:
    # 1. Initialize decomposer
    # 2. Decompose the query into sub-tasks
    # 3. Update state with task list
    # 4. Reset task index to 0
    # 5. Return updated state

    # Placeholder: just pass through
    # return state

    # Example implementation:
    # # Initialize decomposer
    # decomposer = Decomposer(llm_client=None, max_subtasks=5)  # TODO: inject LLM
    #
    # # Decompose the query
    # sub_queries = decomposer.decompose(state.query)
    #
    # # Update state with tasks
    # return AgentState(
    #     query=state.query,
    #     conversation=state.conversation,
    #     tasks=sub_queries,
    #     current_task_index=0,  # Start at first task
    #     retrieved=state.retrieved,
    #     verified=state.verified,
    #     answer=state.answer,
    #     iteration=state.iteration,
    #     memory={
    #         **state.memory,
    #         'decomposed': True,
    #         'num_tasks': len(sub_queries)
    #     }
    # )

    return state


# HELPFUL RESOURCES:
# - LangGraph conditional edges
# - Query decomposition strategies
# - Task planning in AI agents
#
# TIPS:
# - This node typically runs after conversation
# - May return just one task if query is simple
# - Tasks can be processed sequentially or in parallel
# - Store decomposition metadata in state.memory
# - Consider adding task dependencies in memory
# - For Simple Mode, this node might be skipped
# - Log the decomposition for debugging
