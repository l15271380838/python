from typing import AsyncGenerator
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.ai.llm import llm, basic_chat_chain


class AIChatService:

    async def chat(self, message: str) -> str:
        """单轮对话，返回完整回复"""
        result = await basic_chat_chain.ainvoke({"message": message})
        return result

    async def chat_stream(self, message: str) -> AsyncGenerator[str, None]:
        """单轮对话，流式返回"""
        async for chunk in basic_chat_chain.astream({"message": message}):
            yield chunk

    async def chat_with_history(
        self,
        message: str,
        history: list[dict],
        system_prompt: str = "你是一个有帮助的 AI 助手。",
    ) -> str:
        """多轮对话（历史消息从数据库传入）"""
        messages = [SystemMessage(content=system_prompt)]

        # 把历史消息转成 LangChain 消息格式
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=message))

        response = await llm.ainvoke(messages)
        return response.content
