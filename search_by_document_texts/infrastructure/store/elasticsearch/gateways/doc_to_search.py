from typing import List

from .base import Gateway
from search_by_document_texts.сore.protocols import DocToSearchGateway
from search_by_document_texts.сore.entities import DocToSearch, DocumentId


class DocToSearchGatewayImpl(Gateway, DocToSearchGateway):
    async def create(self, doc: DocToSearch):
        await self._connect.index(  # type: ignore
            index=self._el_settings.doc_index,
            body={
                "id": doc.id,
                "text": doc.text,
            },
        )

    async def search(self, text: str) -> List[DocToSearch]:
        query = {"query": {"match": {"text": text}}}
        response = await self._connect.search(  # type: ignore
            index=self._el_settings.doc_index, body=query, size=20
        )
        doc_entities = []
        for doc in response["hits"]["hits"]:
            doc = doc["_source"]
            doc_entity = DocToSearch(doc["id"], doc["text"])
            doc_entities.append(doc_entity)
        return doc_entities

    async def delete_by_doc_id(self, doc_id: DocumentId):
        query = {"query": {"match": {"id": doc_id}}}
        await self._connect.delete_by_query(  # type: ignore
            index=self._el_settings.doc_index, body=query
        )
