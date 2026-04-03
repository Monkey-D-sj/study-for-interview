from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from packages.agents.interview.sub_graphs.project_inspect.nodes.analyze import \
 analyze_node, finish_node
from packages.agents.interview.sub_graphs.project_inspect.nodes.ask_answer import \
 ask_answer_node
from packages.agents.interview.sub_graphs.project_inspect.nodes.ask_detail import \
 ask_detail_node
from packages.agents.interview.sub_graphs.project_inspect.nodes.project_ask import \
	project_ask_node
from packages.agents.interview.sub_graphs.project_inspect.state import ProjectInspectState
from packages.agents.interview.types import ConditionEnum

workflow = StateGraph(ProjectInspectState)
(workflow.add_node(project_ask_node)
 .add_node(ask_answer_node)
 .add_node(analyze_node)
 .add_node(ask_detail_node)
 .add_edge(START, "project_ask_node")
 .add_edge("project_ask_node", "ask_answer_node")
 .add_edge("ask_answer_node", "analyze_node")
 .add_conditional_edges("analyze_node", finish_node, {
    ConditionEnum.LOOP: "ask_detail_node",
    ConditionEnum.PASS: END
 })
 .add_edge("ask_detail_node", "ask_answer_node")
 )

checkpointer = InMemorySaver()
project_inspect_sub_graph = workflow.compile(checkpointer=checkpointer)
