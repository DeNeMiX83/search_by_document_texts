from typing import Callable
from elasticsearch import AsyncElasticsearch
from search_by_document_texts.config.settings import ElasticsearchSettings


def create_elasticsearch_connect_factory(
    es_settings: ElasticsearchSettings,
) -> Callable[..., AsyncElasticsearch]:
    def _connect():
        con = AsyncElasticsearch(
            hosts=es_settings.url,
            http_auth=(es_settings.user, es_settings.password),
            verify_certs=False,
        )

        return con

    return _connect
