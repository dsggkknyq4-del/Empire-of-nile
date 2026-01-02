from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.models import Conversation, Message
from ...shared.ai.client import ai_client

SYSTEM_PROMPT = """You are a helpful language tutor. 
Your goal is to converse with the user in the target language {lang}.
If the user makes a mistake, gently correct them in a separate 'meta' field if possible, or just naturally in the response.
Keep responses concise and encouraging."""

async def send_message(
    conversation_id: str, 
    user_content: str, 
    db: AsyncSession
) -> Message:
    # Get conversation
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    conversation = result.scalars().first()
    if not conversation:
        raise ValueError("Conversation not found")

    # Add User Message
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=user_content
    )
    db.add(user_msg)
    await db.commit()
    
    # Retrieve Context (Last 10 messages)
    # Note: In a real app we'd filter by time/count more robustly
    history_query = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at).limit(10)
    history_result = await db.execute(history_query)
    history_msgs = history_result.scalars().all()
    
    # Construct Prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(lang=conversation.language_code)}]
    for msg in history_msgs:
        messages.append({"role": "user" if msg.role == "user" else "assistant", "content": msg.content})
    
    # Call AI
    ai_response_text = await ai_client.get_chat_completion(messages, request_id=f"conv-{conversation_id}")
    
    # Helper: Simple parsing if we wanted JSON corrections, but for MVP text is fine.
    # Future: Prompt engineering to return JSON with {response, correction}
    
    # Save Assistant Message
    bot_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response_text,
        meta={
            "correction": "None (Standard Response)",
            "disclaimer": "This is an AI-generated educational response."
        }
    )
    db.add(bot_msg)
    await db.commit()
    await db.refresh(bot_msg)
    
    return bot_msg
