from typing import List
from sqlalchemy import select
from .base import Gateway
from search_by_document_texts.сore.protocols import RubricGateway
from search_by_document_texts.сore.entities import Rubric


class RubricGatewayImpl(Gateway, RubricGateway):
    async def get_by_names(self, names: List[str]) -> List[Rubric]:
        stmt = select(Rubric).where(Rubric.name.in_(names))  # type: ignore
        result = await self._session.execute(stmt)
        return [r[0] for r in result.fetchall()]
