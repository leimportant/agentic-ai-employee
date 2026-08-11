from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.modules.models.knowledge_base import KnowledgeBase
from app.modules.models.kb_document import KbDocument


async def list_knowledge_bases(db: AsyncSession, tenant_id: UUID, ai_agent_id: UUID | None = None):
    stmt = select(KnowledgeBase).where(
        KnowledgeBase.tenant_id == tenant_id,
        KnowledgeBase.deleted_at.is_(None),
    )
    if ai_agent_id:
        stmt = stmt.where(KnowledgeBase.ai_agent_id == ai_agent_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_knowledge_base(db: AsyncSession, tenant_id: UUID, kb_id: UUID):
    result = await db.execute(
        select(KnowledgeBase).where(
            KnowledgeBase.id == kb_id,
            KnowledgeBase.tenant_id == tenant_id,
            KnowledgeBase.deleted_at.is_(None),
        )
    )
    kb = result.scalar_one_or_none()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base tidak ditemukan")
    return kb


async def create_knowledge_base(db: AsyncSession, tenant_id: UUID, ai_agent_id: UUID, name: str):
    kb = KnowledgeBase(id=uuid4(), tenant_id=tenant_id, ai_agent_id=ai_agent_id, name=name)
    db.add(kb)
    await db.commit()
    await db.refresh(kb)
    return kb


async def update_knowledge_base(db: AsyncSession, tenant_id: UUID, kb_id: UUID, name: str | None):
    kb = await get_knowledge_base(db, tenant_id, kb_id)
    if name is not None:
        kb.name = name
    await db.commit()
    await db.refresh(kb)
    return kb


async def delete_knowledge_base(db: AsyncSession, tenant_id: UUID, kb_id: UUID):
    from datetime import datetime
    kb = await get_knowledge_base(db, tenant_id, kb_id)
    kb.deleted_at = datetime.utcnow()
    await db.commit()
    return {"message": "Knowledge base dihapus"}


# --- Documents ---

async def list_documents(db: AsyncSession, kb_id: UUID):
    result = await db.execute(
        select(KbDocument).where(
            KbDocument.knowledge_base_id == kb_id,
            KbDocument.deleted_at.is_(None),
        )
    )
    return result.scalars().all()


async def create_document(db: AsyncSession, kb_id: UUID, title: str, content: str):
    doc = KbDocument(id=uuid4(), knowledge_base_id=kb_id, title=title, content=content)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def delete_document(db: AsyncSession, kb_id: UUID, doc_id: UUID):
    from datetime import datetime
    result = await db.execute(
        select(KbDocument).where(KbDocument.id == doc_id, KbDocument.knowledge_base_id == kb_id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan")
    doc.deleted_at = datetime.utcnow()
    await db.commit()
    return {"message": "Dokumen dihapus"}
