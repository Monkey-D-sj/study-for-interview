from typing import  Any, Generator
from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Checkpointer, Command
from langgraph.typing import InputT

from packages.agents.teacher.nodes.intend import \
    intend_node, finish_intend
from packages.agents.teacher.nodes.practice import practice
from packages.agents.teacher.nodes.evaluate import evaluate
from packages.agents.teacher.state import TeacherState

workflow = StateGraph(TeacherState)

(workflow
 .add_node(intend_node)
 .add_node(evaluate)
 .add_node(practice)
 .add_edge(START, "intend_node")
 # .add_edge("intend_node", "practice")
 # .add_edge("practice", "evaluate")
 # .add_edge("evaluate", END)
 .add_conditional_edges("intend_node", finish_intend, {
    "continue": END,
    "loop": "intend_node"
})
)

def run_teacher_agent(user_input: str, checkpointer: Checkpointer, thread_id: str = "", resume: bool = False):
    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    teacher_agent = workflow.compile(checkpointer=checkpointer)
    agent_input: InputT | Command = Command(resume=user_input) if resume else {"user_input": user_input}

    response = teacher_agent.invoke(agent_input, config=config)
    print('response', response)
    return response

    # for chunk in teacher_agent.stream(
    #         agent_input,
    #         config=config,
    #         stream_mode=["updates", "custom"],
    #         version="v2"
    # ):
    #     if chunk["type"] == "custom":
    #         print(chunk["data"])
    #         yield chunk["data"]

