from pydantic import BaseModel
from typing import List
from datetime import date, datetime


class Rubrics(BaseModel):
    name: str


class Document(BaseModel):
    rubrics: List[Rubrics]
    text: str
    created_date: date = datetime.now().date()
