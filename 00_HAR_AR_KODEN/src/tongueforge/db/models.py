import uuid
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from ...shared.db.base import Base

class Conversation(Base):
    __tablename__ = "tf_conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # Linking loosely to shared user ID
    language_code: Mapped[str] = mapped_column(String) # e.g. "es", "fr"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="conversation", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "tf_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tf_conversations.id"))
    role: Mapped[str] = mapped_column(String) # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Optional metadata (corrections, translations)
    meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
