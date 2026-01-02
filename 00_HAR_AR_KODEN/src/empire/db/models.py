import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from ...shared.db.base import Base

class Dynasty(Base):
    __tablename__ = "en_dynasties"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    seed: Mapped[int] = mapped_column(Integer, default=12345)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    states: Mapped[list["GameState"]] = relationship("GameState", back_populates="dynasty", order_by="GameState.year")

class GameState(Base):
    __tablename__ = "en_game_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dynasty_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("en_dynasties.id"))
    year: Mapped[int] = mapped_column(Integer) # Turn number
    season: Mapped[str] = mapped_column(String) # inundation, growing, harvest
    
    # Store resources as JSON for flexibility, or could use columns
    economy: Mapped[dict] = mapped_column(JSON) # {gold: 100, food: 200, population: 50}
    
    last_event_log: Mapped[dict | None] = mapped_column(JSON, nullable=True) # {event: "Flooding", effect: "-10 food"}

    dynasty: Mapped["Dynasty"] = relationship("Dynasty", back_populates="states")
