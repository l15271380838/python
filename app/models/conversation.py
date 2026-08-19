from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# TYPE_CHECKING 用于解决循环导入问题
# 只在类型检查时导入，运行时不导入
if TYPE_CHECKING:
    from app.models.message import Message


class Conversation(Base):
    __tablename__ = "conversations"

    # Mapped[类型] 是 SQLAlchemy 2.0 的新语法
    # 对应 Prisma schema 里的字段定义：
    # id       Int      @id @default(autoincrement())
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # title    String   @db.VarChar(255)
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="新对话")

    # summary  String?  (可选字段)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # createdAt DateTime @default(now())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # updatedAt DateTime @updatedAt
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # 关联关系，对应 Prisma 的 messages Message[]
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",  # 删除会话时级联删除消息
        order_by="Message.created_at",
    )

    def __repr__(self) -> str:
        return f"<Conversation id={self.id} title={self.title}>"
