from .base import Hаndler
from search_by_document_texts.сore import dto
from search_by_document_texts.сore.protocols import (
    DocGateway,
    Commiter,
    DocToSearchGateway,
)


class DeleteDocHandler(Hаndler[dto.DocumentDelete, None]):
    def __init__(
        self,
        document_gateway: DocGateway,
        doc_to_search_gateway: DocToSearchGateway,
        commiter: Commiter,
    ):
        self._document_gateway = document_gateway
        self._doc_to_search_gateway = doc_to_search_gateway
        self._commiter = commiter

    async def execute(self, doc: dto.DocumentDelete):
        await self._document_gateway.delete_by_id(doc.id)
        await self._commiter.commit()
        await self._doc_to_search_gateway.delete_by_doc_id(doc.id)
