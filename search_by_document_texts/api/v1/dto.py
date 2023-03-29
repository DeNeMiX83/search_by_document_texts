from search_by_document_texts.сore.dto import (
    DocumentCreate as DocumentCreate_,
    QueryForSearchDoc as QueryForSearchDoc_,
    DocumentDelete as DocumentDelete_,
    Rubric as Rubric_,
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


class QueryForSearchDoc(QueryForSearchDoc_):
    ...


class DocumentDelete(DocumentDelete_):
    ...


class Rubric(Rubric_):
    ...
