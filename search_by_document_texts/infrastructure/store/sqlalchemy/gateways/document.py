from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from .base import Gateway
from search_by_document_texts.сore.protocols import DocGateway
from search_by_document_texts.сore.entities import Document, DocumentId


class DocGatewayImpl(Gateway, DocGateway):
    async def get(self, id: DocumentId):
        stmt = (
            select(Document)
            .where(Document.id == id)  # type: ignore
            .options(joinedload(Document.rubrics))  # type: ignore
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create(self, doc: Document):
        self._session.add(doc)
        await self._try_exc_flush()

    async def update(self, doc: Document):
        await self._session.execute(
            update(Document)
            .where(Document.id == doc.id)  # type: ignore
            .values(
                rubrics=doc.rubrics,
                text=doc.text,
                created_date=doc.created_date,
            )
        )

    async def delete_by_id(self, doc_id: DocumentId):
        stmt = delete(Document).where(Document.id == doc_id)  # type: ignore
        await self._session.execute(stmt)
