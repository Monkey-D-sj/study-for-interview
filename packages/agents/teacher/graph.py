from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Checkpointer

from packages.agents.teacher.nodes.intend import intend_node
from packages.agents.teacher.nodes.practice import practice
from packages.agents.teacher.nodes.evaluate import evaluate
from packages.agents.teacher.state import TeacherState

workflow = StateGraph(TeacherState)

(workflow
 .add_node(intend_node)
 .add_node(evaluate)
 .add_node(practice)
 .add_edge(START, "intend_node")
 .add_edge("intend_node", "practice")
 .add_edge("practice", "evaluate")
 .add_edge("evaluate", END)
)


teacher_agent = workflow.compile()

async def run_teacher_agent(user_input: str, checkpointer: Checkpointer, thread_id: str = ""):
    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    message = HumanMessage(content=user_input)

    state = await teacher_agent.invoke(message, config=config, checkpointer=checkpointer)
    return state

