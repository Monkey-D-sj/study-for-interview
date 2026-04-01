from typing import  Any, Generator

from langchain_core.messages import AIMessage, \
    AIMessageChunk
from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Checkpointer, Command
from langgraph.typing import InputT

from packages.agents.interview.nodes.examiner import \
    examiner, collect_answer
from packages.agents.interview.nodes.intend import \
    intend_node, finish_intend, intend_input_node
from packages.agents.interview.nodes.evaluate import \
    evaluate, evaluate_pass
from packages.agents.interview.state import TeacherState

workflow = StateGraph(TeacherState)

(workflow
 .add_node(intend_node)
 .add_node(intend_input_node)
 .add_node(examiner)
 .add_node(collect_answer)
 .add_node(evaluate)
 .add_edge(START, "intend_node")
 .add_edge("intend_node", "intend_input_node")
 .add_conditional_edges("intend_input_node", finish_intend, {
    "continue": "examiner",
    "loop": "intend_node"
})
 .add_edge("examiner", "collect_answer")
 .add_edge("collect_answer", "evaluate")
 .add_conditional_edges("evaluate", evaluate_pass, {
    "pass": END,
    "fail": "examiner"
})
)

def run_teacher_agent(user_input: str, checkpointer: Checkpointer, thread_id: str = "", resume: bool = False):
    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    print(resume)
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
            print('custom', data)
            yield data
        elif chunk["type"] == "messages":
            message_chunk, metadata = data
            # print(message_chunk, metadata)
            # print('\n')
            if isinstance(message_chunk, AIMessageChunk):
                print(message_chunk)
            if message_chunk.content:
                print('messages', message_chunk.content)
                yield message_chunk.content

        else:
            if "__interrupt__" in data:
                print('interrupt', data["__interrupt__"][0].value)
                yield data["__interrupt__"][0].value


