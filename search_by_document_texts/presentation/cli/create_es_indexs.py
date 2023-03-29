import os
import asyncio
from elasticsearch import AsyncElasticsearch

from search_by_document_texts.config.settings import ElasticsearchSettings
from search_by_document_texts.infrastructure.store.elasticsearch.connect import (  # noqa E501
    create_elasticsearch_connect_factory,
)


async def mapping_doc(conn: AsyncElasticsearch, index: str):
    mapping = {
        "properties": {  # noqa
            "id": {"type": "integer"},
            "text": {"type": "text"},
        }
    }
    await conn.indices.create(index=index, body={"mappings": mapping})  # type: ignore  # noqa E501


async def mapping(
    conn: AsyncElasticsearch, es_settings: ElasticsearchSettings
):
    await mapping_doc(conn, es_settings.doc_index)


if __name__ == "__main__":
    el_settings = ElasticsearchSettings()
    el_settings.host = "localhost"
    el_settings.port = os.getenv("ELASTIC_HOST_PORT")

    conn = create_elasticsearch_connect_factory(el_settings)()

    asyncio.run(mapping(conn, el_settings))
