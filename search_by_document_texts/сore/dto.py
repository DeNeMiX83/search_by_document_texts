from typing import List
from pydantic import BaseModel
from datetime import datetime

from .entities import DocumentId


class Rubric(BaseModel):
    name: str


class DocumentCreate(BaseModel):
    rubrics: List[Rubric]
    text: str
    created_date: datetime = datetime.now()


class DocumentDelete(BaseModel):
    id: DocumentId


class QueryForSearchDoc(BaseModel):
    text: str
