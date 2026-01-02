from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from ...shared.db.base import get_db_session
from ..db.models import User, UserProfile
from ..api.schemas import AnalysisRequest, AnalysisResponse
from ..services.analysis_service import run_finance_analysis
from .dependencies import get_current_user

router = APIRouter()

@router.post("/finance", response_model=AnalysisResponse)
async def create_analysis(
    request: AnalysisRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db_session)
):
    # Ensure profile exists
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(status_code=400, detail="User profile required for analysis")
    
    return await run_finance_analysis(current_user.id, request, profile, db)
