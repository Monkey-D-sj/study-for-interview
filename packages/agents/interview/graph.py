from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Checkpointer, Command
from langgraph.typing import InputT

from packages.agents.interview.nodes.first_interview import \
    first_interview, collect_answer, finish_first_interview
from packages.agents.interview.nodes.intend import \
    intend_node, finish_intend, intend_input_node
from packages.agents.interview.nodes.evaluate import \
    evaluate
from packages.agents.interview.nodes.second_interview import \
    second_interview
from packages.agents.interview.types import InterviewState, \
    ConditionEnum

workflow = StateGraph(InterviewState)

(workflow
 .add_node(intend_node)
 .add_node(intend_input_node)
 .add_node(first_interview)
 .add_node(second_interview)
 .add_node(collect_answer)
 .add_node(evaluate)
 .add_edge(START, "intend_node")
 .add_edge("intend_node", "intend_input_node")
 .add_conditional_edges("intend_input_node", finish_intend, {
    ConditionEnum.PASS: "first_interview",
    ConditionEnum.LOOP: "intend_node"
})
 .add_edge("first_interview", "collect_answer")
 .add_edge("collect_answer", "evaluate")
 .add_conditional_edges("evaluate", finish_first_interview, {
    ConditionEnum.FAIL: END,
    ConditionEnum.LOOP: "first_interview",
    ConditionEnum.PASS: "second_interview"
})
)

custom_output_nodes = {"first_interview", "evaluate"}

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
            # 跳过自定义输出节点
            if metadata["langgraph_node"] in custom_output_nodes:
                continue
            if message_chunk.content:
                print('messages', message_chunk.content)
                yield message_chunk.content
        else:
            if "__interrupt__" in data:
                print('interrupt', data["__interrupt__"][0].value)
                yield data["__interrupt__"][0].value


