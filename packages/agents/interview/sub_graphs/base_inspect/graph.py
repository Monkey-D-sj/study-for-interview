from langgraph.constants import START, END
from langgraph.graph import StateGraph

from packages.agents.interview.sub_graphs.base_inspect.nodes.analyze import \
	analyze_base_node, is_passed
from packages.agents.interview.sub_graphs.base_inspect.nodes.base_ask import \
	base_ask_node
from packages.agents.interview.sub_graphs.base_inspect.nodes.user_input import \
	user_input_node
from packages.agents.interview.sub_graphs.base_inspect.state import \
	BaseInspectState
from packages.agents.interview.types import ConditionEnum

workflow = StateGraph(BaseInspectState)

(workflow.add_node(base_ask_node)
 .add_node(user_input_node)
 .add_node(analyze_base_node)
 .add_edge(START, "base_ask_node")
 .add_edge("base_ask_node", "user_input_node")
 .add_edge("user_input_node", "analyze_base_node")
 .add_conditional_edges("analyze_base_node", is_passed, {
 	ConditionEnum.PASS: END,
 	ConditionEnum.LOOP: "base_ask_node",
 })
)

base_inspect_sub_graph = workflow.compile()
