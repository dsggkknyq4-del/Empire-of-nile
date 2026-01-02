from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

# Chat
class ConversationCreate(BaseModel):
    language_code: str = Field(..., min_length=2, max_length=5)

class MessageCreate(BaseModel):
    content: str
    
class MessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime
    meta: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: uuid.UUID
    language_code: str
    created_at: datetime
    
    class Config:
        from_attributes = True
