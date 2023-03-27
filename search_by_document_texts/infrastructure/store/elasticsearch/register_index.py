import asyncio
from elasticsearch import AsyncElasticsearch

from search_by_document_texts.config.settings import ElasticsearchSettings


async def mapping_doc(conn: AsyncElasticsearch, index: str):
    mapping = {
        "properties": {  # noqa
            "id": {"type": "integer"},
            "text": {"type": "text"},
        }
    }
    await conn.indices.create(index=index, body={"mappings": mapping})


async def mapping(
    conn: AsyncElasticsearch, es_settings: ElasticsearchSettings
):
    await mapping_doc(conn, es_settings.doc_index)


if __name__ == "__main__":
    from search_by_document_texts.infrastructure.store.elasticsearch.connect import (  # noqa E501
        create_elasticsearch_connect_factory,
    )
    import os

    with open("deploy/.env.dev") as f:
        for line in f:
            if "=" in line:
                key, value = map(lambda x: x.strip(), line.split("="))
                os.environ[key] = value

    el_settings = ElasticsearchSettings()
    conn = create_elasticsearch_connect_factory(el_settings)()

    asyncio.run(mapping(conn, el_settings))
