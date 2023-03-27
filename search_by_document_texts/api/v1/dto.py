from search_by_document_texts.сore.dto import Document as Document_


class Document(Document_):
    class Config:
        schema_extra = {
            "example": {
                "rubrics": [
                    {
                        "name": "спорт"
                    }
                ],
                "text": "example text",
            }
        }
        exclude = {"created_date"}
