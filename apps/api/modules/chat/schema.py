from pydantic import BaseModel


class InterviewChatRequest(BaseModel):
    """
    面试聊天请求
    """
    user_input: str
    session_id: str = None
    resume: bool = False
