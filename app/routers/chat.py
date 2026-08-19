import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_chat import AIChatService
from app.services.conversation import ConversationService

router = APIRouter(prefix="/chat", tags=["AI 对话"])


# 接口一：普通对话（非流式，等全部生成完再返回）
@router.post("/", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    ai_service = AIChatService()
    conv_service = ConversationService(db)

    history = []
    if body.conversation_id:
        messages = await conv_service.get_messages(body.conversation_id)
        history = [{"role": m.role, "content": m.content} for m in messages]

    result = await ai_service.chat_with_history(
        message=body.message,
        history=history,
        system_prompt=body.system_prompt,
    )

    # 保存消息到数据库
    if body.conversation_id:
        await conv_service.add_message(body.conversation_id, "user", body.message)
        await conv_service.add_message(body.conversation_id, "assistant", result)

    return {"content": result, "conversation_id": body.conversation_id}


# 接口二：流式对话（SSE）
@router.post("/stream")
async def chat_stream(body: ChatRequest):
    """
    流式对话接口，用 SSE 返回
    对应 NestJS 版的 @Sse() 装饰器接口
    """

    ai_service = AIChatService()

    async def generate():
        """
        异步生成器函数，yield 每一个 SSE 事件
        FastAPI 的 StreamingResponse 会把这个生成器的每次 yield 发给客户端
        """
        try:
            async for chunk in ai_service.chat_stream(body.message):
                if chunk:
                    # SSE 格式：data: 内容\n\n
                    # 内容用 JSON 包一层，方便前端解析
                    data = json.dumps({"content": chunk}, ensure_ascii=False)
                    yield f"data: {data}\n\n"

            # 发送结束标记
            yield f"data: {json.dumps({'content': '[DONE]'})}\n\n"

        except Exception as e:
            # 发生错误时，向客户端发送错误信息
            error_data = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 告诉 Nginx 不要缓冲（部署时需要）
        },
    )
