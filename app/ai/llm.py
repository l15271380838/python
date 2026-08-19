from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings


# 全局 LLM 实例，整个项目共用
llm = ChatOllama(
    base_url=settings.ollama_base_url,
    model=settings.model_name,
    temperature=0.7,
    num_predict=2048,
)

# 基础对话 chain
basic_chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个有帮助的 AI 助手。"),
        ("human", "{message}"),
    ]
)

basic_chat_chain = basic_chat_prompt | llm | StrOutputParser()
