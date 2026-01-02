from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

# Auth
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Profile
class UserProfileBase(BaseModel):
    risk_level: str = Field(..., pattern="^(low|med|high)$")
    goals: str
    currency: str = "USD"
    country: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    user_id: uuid.UUID
    
    class Config:
        from_attributes = True

# Analysis
class AnalysisRequest(BaseModel):
    context: str
    inputs: Dict[str, Any]

class AnalysisResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    summary: str
    details: Dict[str, Any]
    disclaimer_version: str

    class Config:
        from_attributes = True
