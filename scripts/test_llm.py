import sys
from pathlib import Path

# 将项目根目录加入搜索路径
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from app.ai.llm import llm
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


async def test():
    response = await llm.ainvoke(
        [
            SystemMessage(content="你是一个专业的 Python 教师"),
            HumanMessage(content="什么是装饰器"),
            AIMessage(content="装饰器是一种包装函数的语法糖..."),
        ]
    )
    print("模型回复: ", response.content)
    print("消息类型: ", type(response))


asyncio.run(test())
