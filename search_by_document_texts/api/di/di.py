from fastapi import FastAPI
from search_by_document_texts.infrastructure.store.sqlalchemy.connect import (
    create_session_factory,
)
from search_by_document_texts.infrastructure.store.elasticsearch.connect import (  # noqa E501
    create_elasticsearch_connect_factory,
)
from search_by_document_texts.config.settings import Settings
from search_by_document_texts.api.di.stubs import (
    provide_sqlalchemy_session_stub,
    provide_elasticsearch_conn_stub,
    provide_settings_stub,
    provide_create_doc_handler_stub,
    provide_search_doc_handler_stub,
    provide_delete_doc_handler_stub,
)
from search_by_document_texts.api.di.provides import (
    provide_create_doc_handler,
    provide_search_doc_handler,
    provide_delete_doc_handler,
)


def setup_di(app: FastAPI, settings: Settings):
    session_factory = create_session_factory(settings.postgres.url)
    alasticsearch_conn = create_elasticsearch_connect_factory(
        settings.elasticsearch
    )

    app.dependency_overrides.update(
        {
            provide_sqlalchemy_session_stub: session_factory,
            provide_elasticsearch_conn_stub: alasticsearch_conn,
            provide_settings_stub: lambda: settings,
        }
    )
    app.dependency_overrides.update(
        {
            provide_create_doc_handler_stub: provide_create_doc_handler,
            provide_search_doc_handler_stub: provide_search_doc_handler,
            provide_delete_doc_handler_stub: provide_delete_doc_handler,
        }
    )
