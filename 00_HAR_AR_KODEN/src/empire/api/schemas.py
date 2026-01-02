from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

# Game
class DynastyCreate(BaseModel):
    name: str
    seed: Optional[int] = None

class DynastyResponse(BaseModel):
    id: uuid.UUID
    name: str
    seed: int
    created_at: datetime
    class Config:
        from_attributes = True

class GameStateResponse(BaseModel):
    id: uuid.UUID
    dynasty_id: uuid.UUID
    year: int
    season: str
    economy: Dict[str, int]
    last_event_log: Optional[Dict[str, Any]] = None
    class Config:
        from_attributes = True

class TurnRequest(BaseModel):
    player_actions: Dict[str, int] # e.g., {allocate_food: 10, build_monument: 1}

class TurnResult(BaseModel):
    state: GameStateResponse
    events: Dict[str, Any]
    class Config:
        from_attributes = True
