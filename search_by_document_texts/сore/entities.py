from typing import NewType, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


RubricId = NewType("RubricId", int)
DocumentId = NewType("DocumentId", int)


@dataclass
class Rubric:
    id: Optional[RubricId] = field(init=False)
    name: str

    def __hash__(self):
        return hash(self.name)


@dataclass
class Document:
    id: Optional[DocumentId] = field(init=False)
    text: str
    created_date: datetime
    rubrics: List[Rubric] = field(default_factory=list)


@dataclass
class DocToSearch:
    id: DocumentId
    text: str
