from typing import List
from pydantic import BaseModel
from datetime import date, datetime

from .entities import DocumentId


class Rubrics(BaseModel):
    name: str


class DocumentCreate(BaseModel):
    rubrics: List[Rubrics]
    text: str
    created_date: date = datetime.now().date()


class DocumentDelete(BaseModel):
    id: DocumentId


class QueryForSearchDoc(BaseModel):
    text: str
