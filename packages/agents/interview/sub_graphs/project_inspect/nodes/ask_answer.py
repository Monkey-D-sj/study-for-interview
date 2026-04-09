from langgraph.types import interrupt

from packages.agents.interview.sub_graphs.project_inspect.state import \
	ProjectInspectState


def ask_answer_node(state: ProjectInspectState):
	answer = interrupt(state["question"])
	return {
		"answer": answer,
	}