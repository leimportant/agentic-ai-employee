"""
WhatsApp Webhook — receives incoming messages from Fonnte/Meta.
Flow: incoming msg → find tenant by phone → find/create conversation → AI reply → send back via WA.
"""
from uuid import UUID, uuid4
from fastapi import APIRouter, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database import get_db
from app.modules.models.tenant import Tenant
from app.modules.models.ai_agent import AiAgent
from app.modules.models.customer import Customer
from app.modules.models.conversation import Conversation
from app.modules.models.message import Message
from app.modules.integrations.whatsapp import send_whatsapp_message

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/whatsapp/{tenant_id}")
async def whatsapp_webhook(tenant_id: UUID, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Webhook URL per tenant: POST /api/v1/webhook/whatsapp/{tenant_id}
    Fonnte sends: { "sender": "6281xxx", "message": "Halo", "name": "John" }
    """
    body = await request.json()

    sender = body.get("sender", "").replace("+", "")
    message = body.get("message", "")
    sender_name = body.get("name", sender)

    if not sender or not message:
        return {"status": "ignored"}

    # Find or create customer
    result = await db.execute(
        select(Customer).where(Customer.tenant_id == tenant_id, Customer.phone == sender)
    )
    customer = result.scalar_one_or_none()
    if not customer:
        customer = Customer(
            id=uuid4(), tenant_id=tenant_id,
            name=sender_name, phone=sender, email=None, channel="whatsapp",
        )
        db.add(customer)
        await db.flush()

    # Find active agent for this tenant (first active CS agent)
    agent_result = await db.execute(
        select(AiAgent).where(
            AiAgent.tenant_id == tenant_id,
            AiAgent.is_active == True,
            AiAgent.type == "customer_service",
        ).limit(1)
    )
    agent = agent_result.scalar_one_or_none()
    if not agent:
        return {"status": "no_active_agent"}

    # Find or create conversation
    convo_result = await db.execute(
        select(Conversation).where(
            Conversation.tenant_id == tenant_id,
            Conversation.customer_id == customer.id,
            Conversation.ai_agent_id == agent.id,
            Conversation.status == "active",
        ).limit(1)
    )
    convo = convo_result.scalar_one_or_none()
    if not convo:
        convo = Conversation(
            id=uuid4(), tenant_id=tenant_id,
            ai_agent_id=agent.id, customer_id=customer.id,
            channel="whatsapp", status="active",
        )
        db.add(convo)
        await db.flush()

    # Save incoming message
    db.add(Message(id=uuid4(), conversation_id=convo.id, role="user", content=message))

    # Generate AI reply (same placeholder as conversations service)
    ai_reply = f"Terima kasih atas pesan Anda. Saya akan membantu terkait: {message[:100]}"

    # Save AI reply
    db.add(Message(id=uuid4(), conversation_id=convo.id, role="assistant", content=ai_reply))
    await db.commit()

    # Send reply via WhatsApp
    await send_whatsapp_message(db, tenant_id, sender, ai_reply)

    return {"status": "replied", "reply": ai_reply}
