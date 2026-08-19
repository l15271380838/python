import sys
from pathlib import Path

# 将项目根目录加入搜索路径
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.ai.llm import llm


async def main():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专业的 {subject} 老师，回答要简洁易懂。"),
            ("human", "{question}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    # 单次调用
    result = await chain.ainvoke(
        {
            "subject": "Python",
            "question": "什么是 f-string？",
        }
    )
    print("单次调用结果：", result)
    print("-" * 40)

    # 批量调用（一次传多个输入）
    results = await chain.abatch(
        [
            {"subject": "Python", "question": "什么是列表？"},
            {"subject": "FastAPI", "question": "什么是路由？"},
        ]
    )
    print("批量调用结果：")
    for r in results:
        print(" ", r[:50], "...")


asyncio.run(main())
