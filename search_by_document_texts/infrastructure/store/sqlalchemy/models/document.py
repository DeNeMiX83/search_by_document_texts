from sqlalchemy import Column, String, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base
from search_by_document_texts.сore import entities

document_rubric = Table(
    "document_rubric",
    Base.metadata,
    Column(
        "document_id", Integer, ForeignKey("document.id", ondelete="CASCADE")  # noqa
    ),
    Column("rubric_id", Integer, ForeignKey("rubric.id")),
)


class Rubric(Base):
    __tablename__ = "rubric"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    created_date = Column(Date, nullable=False)


def rubric_mapping(mapper_registry):
    table = Rubric.__table__
    mapper_registry.map_imperatively(
        entities.Rubric,
        table,
    )


def document_mapping(mapper_registry):
    table = Document.__table__
    mapper_registry.map_imperatively(
        entities.Document,
        table,
        properties={
            "rubrics": relationship(entities.Rubric, secondary=document_rubric)
        },
    )


def mapping():
    mapper_registry = Base.registry
    rubric_mapping(mapper_registry)
    document_mapping(mapper_registry)
