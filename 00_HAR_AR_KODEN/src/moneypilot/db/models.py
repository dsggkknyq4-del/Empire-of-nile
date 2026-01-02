import uuid
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from ...shared.db.base import Base

class User(Base):
    __tablename__ = "mp_users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", uselist=False)
    analyses: Mapped[list["AnalysisResult"]] = relationship("AnalysisResult", back_populates="user")

class UserProfile(Base):
    __tablename__ = "mp_user_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("mp_users.id"), primary_key=True)
    risk_level: Mapped[str] = mapped_column(String) # enum: low, med, high
    goals: Mapped[str] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String, default="USD")
    country: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="profile")

class AnalysisResult(Base):
    __tablename__ = "mp_analysis_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("mp_users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    summary: Mapped[str] = mapped_column(String)
    details: Mapped[dict] = mapped_column(JSON)
    disclaimer_version: Mapped[str] = mapped_column(String)

    user: Mapped["User"] = relationship("User", back_populates="analyses")
