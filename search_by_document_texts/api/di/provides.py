from typing import Callable, Type
from fastapi import Depends
from search_by_document_texts.config.settings import Settings
from sqlalchemy.ext.asyncio import AsyncSession
from search_by_document_texts.infrastructure.store.sqlalchemy import (
    gateways as sqlalchemy_gateways,
)
from elasticsearch import AsyncElasticsearch
from search_by_document_texts.infrastructure.store.elasticsearch import (
    gateways as elasticsearch_gateways,
)

from search_by_document_texts.сore.handlers import CreateDocHandler

from .stubs import (
    provide_sqlalchemy_session_stub,
    provide_elasticsearch_conn_stub,
    provide_settings_stub,
)


def get_sqlalchemy_gateway(
    gateway_type: Type[sqlalchemy_gateways.Gateway],
) -> Callable[[AsyncSession], sqlalchemy_gateways.Gateway]:
    def _get_gateway(
        session: AsyncSession = Depends(provide_sqlalchemy_session_stub),
    ) -> sqlalchemy_gateways.Gateway:
        return gateway_type(session)

    return _get_gateway


def get_elasticsearch_gateway(
    gateway_type: Type[elasticsearch_gateways.Gateway],
) -> Callable[[AsyncElasticsearch], elasticsearch_gateways.Gateway]:
    def _get_gateway(
        conn: AsyncElasticsearch = Depends(provide_elasticsearch_conn_stub),
        settings: Settings = Depends(provide_settings_stub),
    ) -> elasticsearch_gateways.Gateway:
        return gateway_type(conn, settings.elasticsearch)

    return _get_gateway


def provide_create_doc_handler(
    doc_gateway: sqlalchemy_gateways.Gateway = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateways.DocGatewayImpl)
    ),
    rubric_gateway: sqlalchemy_gateways.Gateway = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateways.RubricGatewayImpl)
    ),
    doc_to_search: elasticsearch_gateways.Gateway = Depends(
        get_elasticsearch_gateway(
            elasticsearch_gateways.DocToSearchGatewayImpl
        )
    ),
    commiter: sqlalchemy_gateways.Gateway = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateways.CommiterImpl)
    ),
) -> CreateDocHandler:
    return CreateDocHandler(
        document_gateway=doc_gateway,  # type: ignore
        rubric_gateway=rubric_gateway,  # type: ignore
        doc_to_search_gateway=doc_to_search,  # type: ignore
        commiter=commiter,  # type: ignore
    )
