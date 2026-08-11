from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.modules.models.conversation import Conversation
from app.modules.models.message import Message
from app.modules.models.ai_agent import AiAgent
from app.modules.conversations.schemas import StartConversationRequest


async def list_conversations(db: AsyncSession, tenant_id: UUID, agent_id: UUID = None):
    q = select(Conversation).where(Conversation.tenant_id == tenant_id)
    if agent_id:
        q = q.where(Conversation.ai_agent_id == agent_id)
    q = q.order_by(Conversation.created_at.desc())
    result = await db.execute(q)
    return result.scalars().all()


async def get_conversation(db: AsyncSession, tenant_id: UUID, convo_id: UUID):
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.id == convo_id, Conversation.tenant_id == tenant_id)
    )
    convo = result.scalar_one_or_none()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo


async def start_conversation(db: AsyncSession, tenant_id: UUID, data: StartConversationRequest):
    convo = Conversation(
        id=uuid4(),
        tenant_id=tenant_id,
        ai_agent_id=data.ai_agent_id,
        customer_id=data.customer_id,
        channel=data.channel,
        status="active",
    )
    db.add(convo)
    await db.commit()
    await db.refresh(convo)
    return convo


async def send_message(db: AsyncSession, tenant_id: UUID, convo_id: UUID, content: str):
    """Save user message and generate AI reply."""
    convo = await get_conversation(db, tenant_id, convo_id)

    # Save user message
    user_msg = Message(id=uuid4(), conversation_id=convo_id, role="user", content=content)
    db.add(user_msg)

    # Get agent system prompt
    agent = await db.get(AiAgent, convo.ai_agent_id)
    system_prompt = agent.system_prompt if agent else ""

    # Generate AI reply (placeholder - will integrate LLM later)
    ai_reply = await _generate_reply(db, convo_id, system_prompt, content)

    # Save AI message
    ai_msg = Message(id=uuid4(), conversation_id=convo_id, role="assistant", content=ai_reply)
    db.add(ai_msg)

    await db.commit()
    return {"user_message": content, "ai_reply": ai_reply}


async def _generate_reply(db: AsyncSession, convo_id: UUID, system_prompt: str, user_input: str) -> str:
    """
    Placeholder for AI reply generation.
    TODO: integrate with LLM (Gemini/OpenAI/Groq) + RAG from knowledge base.
    """
    # For now, return a simple echo response
    # In production, this will call the LLM with conversation history + system prompt
    return f"Terima kasih atas pesan Anda. Saya akan membantu terkait: {user_input[:100]}"
