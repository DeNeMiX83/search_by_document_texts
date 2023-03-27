from .base import Gateway
from search_by_document_texts.сore.protocols import DocToSearchGateway
from search_by_document_texts.сore.entities import DocToSearch


class DocToSearchGatewayImpl(Gateway, DocToSearchGateway):
    async def create(self, doc: DocToSearch):
        await self._connect.index(
            index=self._el_settings.doc_index,
            body={
                "id": doc.id,
                "text": doc.text,
            },
        )
