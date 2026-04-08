from langgraph.config import get_stream_writer
from langgraph.types import interrupt

from packages.agents.interview.sub_graphs.project_inspect.state import \
    ProjectInspectState

def project_ask_node(state: ProjectInspectState):
    question = """
    请你介绍一个你最熟悉、最有挑战性的项目
    要求：
    - 必须包含：项目背景、技术架构、你的职责、核心难点
    """
    writer = get_stream_writer()
    writer(question)
    answer = interrupt("")

    return {
        "question": question,
        "answer": answer,
        "dialogue_loop": 0,
    }

