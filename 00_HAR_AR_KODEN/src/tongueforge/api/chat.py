from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from ...shared.db.base import get_db_session
from ..db.models import Conversation, Message
from ..api.schemas import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse
from ..services.chat_service import send_message
from .dependencies import get_current_user_id

router = APIRouter()

@router.post("/conversations", response_model=ConversationResponse)
async def start_conversation(
    conv_data: ConversationCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    new_conv = Conversation(
        user_id=user_id,
        language_code=conv_data.language_code
    )
    db.add(new_conv)
    await db.commit()
    await db.refresh(new_conv)
    return new_conv

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(select(Conversation).where(Conversation.user_id == user_id))
    return result.scalars().all()

@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def post_message(
    conversation_id: uuid.UUID,
    msg_data: MessageCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    # Verify ownership
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    return await send_message(conversation_id, msg_data.content, db)
