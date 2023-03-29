from .base import Hаndler
from search_by_document_texts.сore import dto
from search_by_document_texts.сore.protocols import (
    DocGateway,
    RubricGateway,
    Commiter,
    DocToSearchGateway,
)
from search_by_document_texts.сore.entities import Document, DocToSearch


class CreateDocHandler(Hаndler[dto.Document, None]):
    def __init__(
        self,
        document_gateway: DocGateway,
        rubric_gateway: RubricGateway,
        doc_to_search_gateway: DocToSearchGateway,
        commiter: Commiter,
    ):
        self._document_gateway = document_gateway
        self._rubric_gateway = rubric_gateway
        self._doc_to_search_gateway = doc_to_search_gateway
        self._commiter = commiter

    async def execute(self, doc_dto: dto.Document) -> None:
        rubrics = await self._rubric_gateway.get_by_names(
            [r.name for r in doc_dto.rubrics]
        )
        doc = Document(
            text=doc_dto.text,
            created_date=doc_dto.created_date,
            rubrics=rubrics,
        )
        await self._document_gateway.create(doc)
        await self._commiter.commit()

        doc_to_search = DocToSearch(
            id=doc.id,  # type: ignore
            text=doc_dto.text,
        )
        await self._doc_to_search_gateway.create(doc_to_search)
