from fastapi import APIRouter, Header, Depends
from fastapi.responses import StreamingResponse
from fastapi.sse import EventSourceResponse

from .schema import InterviewChatRequest
from .service import ChatService
from ...core.dependencies import db_dependencies

chat_router = APIRouter(
	prefix="/chat",
	tags=["chat"]
)

@chat_router.post("/interview", response_class=EventSourceResponse)
async def interview_intend(
	request: InterviewChatRequest,
	session_id: str = Header(None, description="会话ID"),
	checkpointer = Depends(db_dependencies.get_checkpointer),
):
	service = ChatService(checkpointer)
	for chunk in service.interview_intend(
			request.user_input,
			session_id
		):
		yield chunk

