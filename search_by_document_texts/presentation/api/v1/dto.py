from typing import List
from pydantic import BaseModel
from datetime import datetime

from search_by_document_texts.сore.dto import (
    DocumentCreate as DocumentCreate_,
    QueryForSearchDoc as QueryForSearchDoc_,
    DocumentDelete as DocumentDelete_,
    Rubric as Rubric_,
)
from search_by_document_texts.сore.entities import (
    Document as DocumentEntity,
    Rubric as RubricEntity,
)


class RubricCreate(Rubric_):
    ...


class Rubric(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, rubric: RubricEntity) -> "Rubric":
        return cls(
            id=rubric.id,  # type: ignore
            name=rubric.name,
        )


class DocumentCreate(DocumentCreate_):
    class Config:
        schema_extra = {
            "example": {
                "rubrics": [{"name": "спорт"}],
                "text": "example text",
            }
        }
        exclude = {"created_date"}


class Document(BaseModel):
    id: int
    rubrics: List[Rubric]
    text: str
    created_date: datetime

    @classmethod
    def from_entity(cls, doc: DocumentEntity) -> "Document":
        return cls(
            id=doc.id,  # type: ignore
            text=doc.text,
            created_date=doc.created_date,
            rubrics=[Rubric.from_entity(r) for r in doc.rubrics],
        )


class QueryForSearchDoc(QueryForSearchDoc_):
    ...


class DocumentDelete(DocumentDelete_):
    ...
