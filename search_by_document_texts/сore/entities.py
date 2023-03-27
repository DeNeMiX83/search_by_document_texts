from typing import NewType, Optional, List
from dataclasses import dataclass, field
from datetime import date


RubricId = NewType("RubricId", int)
DocumentId = NewType("DocumentId", int)


@dataclass
class Rubric:
    id: Optional[RubricId] = field(init=False)
    name: str


@dataclass
class Document:
    id: Optional[DocumentId] = field(init=False)
    rubrics: List[Rubric]
    text: str
    created_date: date


@dataclass
class DocToSearch:
    id: DocumentId
    text: str
