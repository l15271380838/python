from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.conversation import ConversationService
from app.schemas.conversation import (
    CreateConversationRequest,
    ConversationResponse,
    ConversationDetailResponse,
)

router = APIRouter(prefix="/conversations", tags=["会话管理"])


@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    body: CreateConversationRequest,
    db: AsyncSession = Depends(get_db),  # 依赖注入数据库 Session
):
    service = ConversationService(db)
    conversation = await service.create_conversation(body.title)
    return conversation


@router.get("/", response_model=list[ConversationResponse])
async def get_conversations(db: AsyncSession = Depends(get_db)):
    service = ConversationService(db)
    return await service.get_all_conversations()


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db)
    conversation = await service.get_conversation_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="会话不存在")
    return conversation


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db)
    deleted = await service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="会话不存在")
    return {"message": "删除成功"}
