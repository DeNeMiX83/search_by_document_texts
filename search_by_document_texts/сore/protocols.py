from typing import Protocol, List
from .entities import Document, DocumentId, Rubric, DocToSearch


class DocGateway(Protocol):
    async def get(self, doc_id: DocumentId) -> Document:
        raise NotImplementedError

    async def create(self, doc: Document):
        raise NotImplementedError

    async def update(self, doc: Document):
        raise NotImplementedError

    async def delete_by_id(self, doc_id: DocumentId):
        raise NotImplementedError


class RubricGateway(Protocol):
    async def get_by_names(self, names: List[str]) -> List[Rubric]:
        raise NotImplementedError


class DocToSearchGateway(Protocol):
    async def get(self, doc_id: DocumentId) -> DocToSearch:
        raise NotImplementedError

    async def search(self, text: str) -> List[DocToSearch]:
        raise NotImplementedError

    async def create(self, doc: DocToSearch):
        raise NotImplementedError

    async def delete_by_doc_id(self, doc_id: DocumentId):
        raise NotImplementedError


class Commiter(Protocol):
    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
