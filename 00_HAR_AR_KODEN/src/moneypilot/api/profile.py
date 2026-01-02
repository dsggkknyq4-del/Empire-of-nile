from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from ...shared.db.base import get_db_session
from ..db.models import User, UserProfile
from ..api.schemas import UserProfileCreate, UserProfileResponse
from .dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=UserProfileResponse)
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db_session)
):
    query = select(UserProfile).where(UserProfile.user_id == current_user.id)
    result = await db.execute(query)
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/", response_model=UserProfileResponse)
async def upsert_profile(
    profile_data: UserProfileCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db_session)
):
    query = select(UserProfile).where(UserProfile.user_id == current_user.id)
    result = await db.execute(query)
    existing_profile = result.scalars().first()
    
    if existing_profile:
        # Update
        existing_profile.risk_level = profile_data.risk_level
        existing_profile.goals = profile_data.goals
        existing_profile.currency = profile_data.currency
        existing_profile.country = profile_data.country
    else:
        # Create
        new_profile = UserProfile(
            user_id=current_user.id,
            **profile_data.model_dump()
        )
        db.add(new_profile)
        existing_profile = new_profile # use for return
    
    await db.commit()
    await db.refresh(existing_profile)
    return existing_profile
