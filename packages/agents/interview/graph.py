from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Checkpointer, Command
from langgraph.typing import InputT

from packages.agents.interview.sub_graphs.base_inspect.graph import \
    base_inspect_sub_graph
from packages.agents.interview.sub_graphs.project_inspect.graph import \
    project_inspect_sub_graph
from packages.agents.interview.nodes.intend import \
    intend_node, finish_intend, intend_input_node
from packages.agents.interview.types import InterviewState, \
    ConditionEnum

workflow = StateGraph(InterviewState)

def base_inspect_node(state: InterviewState):
    sub_graph_output = base_inspect_sub_graph.invoke({
        "position": state["position"],
        "level": state.get("level", "junior"),
        "used_question_ids": [],  # 初始化已出题ID列表
    })
    print(sub_graph_output)
    return {
        "base_passed": sub_graph_output["is_passed"],
    }

def can_go_second_interview(state: InterviewState):
    if state["base_passed"]:
        return ConditionEnum.PASS
    return ConditionEnum.FAIL


def project_inspect_node(state: InterviewState):
    sub_graph_output = project_inspect_sub_graph.invoke({
        "position": state["position"],
    })
    print(sub_graph_output)
    return {
        "question": sub_graph_output["question"],
    }

(workflow
 .add_node(intend_node)
 .add_node(intend_input_node)
 .add_node(base_inspect_node)
 .add_node(project_inspect_node)
 .add_edge(START, "intend_node")
 .add_edge("intend_node", "intend_input_node")
 .add_conditional_edges("intend_input_node", finish_intend, {
    ConditionEnum.PASS: "base_inspect_node",
    ConditionEnum.LOOP: "intend_node"
})
 .add_conditional_edges("base_inspect_node", can_go_second_interview, {
    ConditionEnum.PASS: "project_inspect_node",
    ConditionEnum.FAIL: END,
})
)


def run_teacher_agent(user_input: str, checkpointer: Checkpointer, thread_id: str = "", resume: bool = False):
    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    teacher_agent = workflow.compile(checkpointer=checkpointer)

    # 导出Mermaid代码
    mermaid_code = teacher_agent.get_graph().draw_mermaid()
    # 保存到文件
    with open("graph.mmd", "w") as f:
        f.write(mermaid_code)

    agent_input: InputT | Command = Command(resume=user_input, update={
        "user_input": user_input
    }) if resume else {"user_input": user_input}

    for chunk in teacher_agent.stream(
            agent_input,
            config=config,
            stream_mode=["updates", "custom", "messages"],
            version="v2"
    ):
        data = chunk["data"]
        if chunk["type"] == "custom":
            yield data
        elif chunk["type"] == "messages":
            message_chunk, metadata = data
            if message_chunk.content:
                print('messages', message_chunk.content)
                yield message_chunk.content
        else:
            if "__interrupt__" in data:
                print('interrupt', data["__interrupt__"][0].value)
                yield data["__interrupt__"][0].value


