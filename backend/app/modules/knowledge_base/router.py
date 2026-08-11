from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.knowledge_base import service, schemas

router = APIRouter(prefix="/knowledge-bases", tags=["knowledge-bases"])


@router.get("", response_model=list[schemas.KBOut])
async def list_kbs(tenant_id: UUID, ai_agent_id: Optional[UUID] = None, db: AsyncSession = Depends(get_db)):
    return await service.list_knowledge_bases(db, tenant_id, ai_agent_id)


@router.get("/{kb_id}", response_model=schemas.KBOut)
async def get_kb(tenant_id: UUID, kb_id: UUID, db: AsyncSession = Depends(get_db)):
    return await service.get_knowledge_base(db, tenant_id, kb_id)


@router.post("", response_model=schemas.KBOut, status_code=201)
async def create_kb(tenant_id: UUID, req: schemas.KBCreateRequest, db: AsyncSession = Depends(get_db)):
    return await service.create_knowledge_base(db, tenant_id, req.ai_agent_id, req.name)


@router.patch("/{kb_id}", response_model=schemas.KBOut)
async def update_kb(tenant_id: UUID, kb_id: UUID, req: schemas.KBUpdateRequest, db: AsyncSession = Depends(get_db)):
    return await service.update_knowledge_base(db, tenant_id, kb_id, req.name)


@router.delete("/{kb_id}")
async def delete_kb(tenant_id: UUID, kb_id: UUID, db: AsyncSession = Depends(get_db)):
    return await service.delete_knowledge_base(db, tenant_id, kb_id)


# --- Documents ---

@router.get("/{kb_id}/documents", response_model=list[schemas.KBDocumentOut])
async def list_docs(kb_id: UUID, db: AsyncSession = Depends(get_db)):
    return await service.list_documents(db, kb_id)


@router.post("/{kb_id}/documents", response_model=schemas.KBDocumentOut, status_code=201)
async def create_doc(kb_id: UUID, req: schemas.KBDocumentCreateRequest, db: AsyncSession = Depends(get_db)):
    return await service.create_document(db, kb_id, req.title, req.content)


@router.delete("/{kb_id}/documents/{doc_id}")
async def delete_doc(kb_id: UUID, doc_id: UUID, db: AsyncSession = Depends(get_db)):
    return await service.delete_document(db, kb_id, doc_id)
