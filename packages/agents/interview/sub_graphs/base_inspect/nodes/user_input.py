from langgraph.types import interrupt

from packages.agents.interview.sub_graphs.base_inspect.state import \
	BaseInspectState


def user_input_node(state: BaseInspectState):
    answer = interrupt("")
    return {
        "answer": answer,
    }