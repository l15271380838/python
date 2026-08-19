from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.models.conversation import Conversation
from app.models.message import Message
from sqlalchemy import select, delete, desc


class ConversationService:
    """
    会话管理 Service
    对应 NestJS 里的 @Injectable() ConversationService
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(self, title: str = "新对话") -> Conversation:
        """创建新会话，对应 Prisma 的 prisma.conversation.create()"""
        conversation = Conversation(title=title)
        self.db.add(conversation)
        await self.db.flush()  # flush 把操作发到数据库但不提交，获取自动生成的 id
        await self.db.refresh(conversation)  # 刷新对象，获取数据库生成的字段
        return conversation

    async def get_conversation_by_id(self, conversation_id: int) -> Conversation | None:
        """按 ID 查询会话，对应 Prisma 的 prisma.conversation.findUnique()"""
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))  # 同时加载关联的消息
        )
        return result.scalar_one_or_none()

    async def get_all_conversations(self) -> list[Conversation]:
        """查询所有会话，对应 Prisma 的 prisma.conversation.findMany()"""
        result = await self.db.execute(
            select(Conversation).order_by(Conversation.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete_conversation(self, conversation_id: int) -> bool:
        """删除会话，对应 Prisma 的 prisma.conversation.delete()"""
        result = await self.db.execute(
            delete(Conversation).where(Conversation.id == conversation_id)
        )
        return result.rowcount > 0

    async def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        """添加一条消息"""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def get_messages(self, conversation_id: int) -> list[Message]:
        """获取会话的所有消息，按时间升序"""
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())


async def get_recent_messages(
    self,
    conversation_id: int,
    limit: int = 20,
) -> list[Message]:
    """
    获取最近 N 条消息，用于多轮对话上下文
    limit 默认 20，即最近 10 轮对话（10 条 user + 10 条 assistant）
    """
    result = await self.db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())  # 先按时间倒序取
        .limit(limit)
    )
    messages = list(result.scalars().all())
    # 反转，让消息按时间正序排列（最新的在最后）
    return list(reversed(messages))


async def count_messages(self, conversation_id: int) -> int:
    """统计会话消息总数"""
    from sqlalchemy import func as sql_func, select

    result = await self.db.execute(
        select(sql_func.count(Message.id)).where(
            Message.conversation_id == conversation_id
        )
    )
    return result.scalar() or 0
