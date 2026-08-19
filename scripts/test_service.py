import sys
from pathlib import Path


import asyncio
from app.ai.llm import llm
from app.services.ai_chat import AIChatService


async def main():
    service = AIChatService()

    # 测试单轮对话
    result = await service.chat("你好，用一句话自我介绍")
    print("单轮对话：", result)

    # 测试多轮对话
    history = [
        {"role": "user", "content": "我叫大伟"},
        {"role": "assistant", "content": "你好，大伟！很高兴认识你。"},
    ]
    result2 = await service.chat_with_history("你还记得我叫什么吗？", history)
    print("多轮对话：", result2)


asyncio.run(main())
