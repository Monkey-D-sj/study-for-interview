import uuid
from fastapi import APIRouter, Header, Depends
from packages.agents.teacher.graph import run_teacher_agent
from .schema import InterviewChatRequest
from ...main import redis_checkpointer

chat_router = APIRouter(
	prefix="/chat",
	tags=["chat"]
)

@chat_router.post("/interview")
async def interview_intend(
	request: InterviewChatRequest,
	session_id: str = Header(None, description="会话ID"),
):
	"""
	询问面试者的意图
	"""
	if session_id is None:
		session_id = str(uuid.uuid4())
	state = await run_teacher_agent(request.user_input, redis_checkpointer, session_id)
	return state
