import sys
from pathlib import Path

# 将项目根目录加入搜索路径
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from app.ai.llm import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.ai.llm import llm


async def main():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个有帮助的 AI 助手。"),
            ("human", "{question}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    print("流式输出开始：")
    # astream 返回一个异步生成器，每次 yield 一个文字片段
    # 对应 NestJS 版的 for await (const chunk of chain.stream(...))
    async for chunk in chain.astream({"question": "用 200 字介绍一下武汉"}):
        print(chunk, end="", flush=True)
        # flush=True 确保立刻输出到终端，不缓冲

    print("\n流式输出结束")


asyncio.run(main())
