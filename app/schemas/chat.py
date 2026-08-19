from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    system_prompt: str = "你是一个有帮助的 AI 助手。"


class ChatResponse(BaseModel):
    content: str
    conversation_id: Optional[int] = None
