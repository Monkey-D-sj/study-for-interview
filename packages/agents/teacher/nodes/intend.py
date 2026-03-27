from langchain_core.messages import SystemMessage
from packages.agents.teacher.model import teacher_model
from packages.agents.teacher.state import TeacherState

intend_system_prompt = """
你是一个资深程序员，熟悉各种技术栈，需要你询问面试者的意图，包括：
- 面试岗位
- 面试职级
- 面试话题
如果没有获取完整信息，可以通过ask_user对话获取。
可用工具: 
- ask_user 询问用户问题
"""

def intend_node(state: TeacherState) -> TeacherState:
    """
    询问面试者的意图
    """
    messages = [
        SystemMessage(content=intend_system_prompt)
    ]

    response = teacher_model.invoke(messages)
    print(response)
    state["intend"] = response.content
    return state
