import uuid

from fastapi.sse import ServerSentEvent
from langgraph.types import Checkpointer

from packages.agents.interview.graph import run_teacher_agent


class ChatService:
	def __init__(self, checkpointer: Checkpointer):
		self.checkpointer = checkpointer

	def interview_intend(self, user_input: str, session_id: str = None, resume: bool = False):
		"""
		询问面试者的意图
		"""
		if session_id is None:
			session_id = str(uuid.uuid4())

		for chunk in run_teacher_agent(
			user_input,
			self.checkpointer,
			session_id,
			resume=resume
		):
			yield ServerSentEvent(data={
				"type": "content",
				"message": chunk
			})

