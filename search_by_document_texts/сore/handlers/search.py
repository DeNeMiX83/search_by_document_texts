from typing import List

from .base import Hаndler
from search_by_document_texts.сore import dto
from search_by_document_texts.сore.protocols import (
    DocGateway,
    DocToSearchGateway,
)
from search_by_document_texts.сore.entities import Document


class SearchDocByQuery(Hаndler[dto.QueryForSearchDoc, List[Document]]):
    def __init__(
        self,
        document_gateway: DocGateway,
        doc_to_search_gateway: DocToSearchGateway,
    ):
        self._document_gateway = document_gateway
        self._doc_to_search_gateway = doc_to_search_gateway

    async def execute(self, query: dto.QueryForSearchDoc) -> List[Document]:
        docs_to_search = await self._doc_to_search_gateway.search(query.text)
        docs = []
        for doc_to_search in docs_to_search:
            doc = await self._document_gateway.get(doc_to_search.id)
            docs.append(doc)
        docs.sort(key=lambda doc: doc.created_date, reverse=True)
        return docs
