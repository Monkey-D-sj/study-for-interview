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
	checkpointer = Depends(db_dependencies.get_checkpointer),
):
	service = ChatService(checkpointer)
	for chunk in service.interview_intend(
			request.user_input,
			request.session_id,
			request.resume
		):
		yield chunk

