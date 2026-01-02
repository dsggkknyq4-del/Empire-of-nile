from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import uuid
import random

from ...shared.db.base import get_db_session
from ..db.models import Dynasty, GameState
from ..api.schemas import DynastyCreate, DynastyResponse, GameStateResponse, TurnRequest, TurnResult
from ..services.engine import process_turn
from .dependencies import get_optional_user_id

router = APIRouter()

@router.post("/game/start", response_model=DynastyResponse)
async def start_game(
    data: DynastyCreate,
    db: AsyncSession = Depends(get_db_session)
):
    seed = data.seed or random.randint(1, 999999)
    new_dynasty = Dynasty(name=data.name, seed=seed)
    db.add(new_dynasty)
    await db.commit()
    await db.refresh(new_dynasty)
    
    # Initial State
    initial_state = GameState(
        dynasty_id=new_dynasty.id,
        year=1,
        season="inundation",
        economy={"gold": 100, "food": 500, "population": 100},
        last_event_log={"event": "Dynasty Founded", "effect": "None"}
    )
    db.add(initial_state)
    await db.commit()
    
    return new_dynasty

@router.get("/game/{dynasty_id}/state", response_model=GameStateResponse)
async def get_state(
    dynasty_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    # Get latest state
    result = await db.execute(
        select(GameState)
        .where(GameState.dynasty_id == dynasty_id)
        .order_by(desc(GameState.year))
        .limit(1)
    )
    state = result.scalars().first()
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")
    return state

@router.post("/game/turn", response_model=TurnResult)
async def advance_turn(
    request: TurnRequest,
    db: AsyncSession = Depends(get_db_session)
):
    # Get Dynasty & Current State
    dynasty = await db.scalar(select(Dynasty).where(Dynasty.id == request.dynasty_id))
    if not dynasty:
        raise HTTPException(status_code=404, detail="Dynasty not found")
        
    current_state = await db.scalar(
        select(GameState)
        .where(GameState.dynasty_id == request.dynasty_id)
        .order_by(desc(GameState.year))
        .limit(1)
    )
    
    # Calculate Next State
    next_state_data = process_turn(current_state, request.player_actions, dynasty.seed)
    
    new_state = GameState(
        dynasty_id=dynasty.id,
        **next_state_data
    )
    
    db.add(new_state)
    await db.commit()
    await db.refresh(new_state)
    
    return {
        "state": new_state,
        "events": next_state_data["last_event_log"],
        "metrics": next_state_data["economy"]
    }
