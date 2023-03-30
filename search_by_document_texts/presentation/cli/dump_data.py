import os
import asyncio
import csv
from datetime import datetime

from search_by_document_texts.config.settings import (
    PostgresSettings,
    ElasticsearchSettings,
)
from search_by_document_texts.infrastructure.store.sqlalchemy.connect import (
    create_session_factory,
)
from search_by_document_texts.infrastructure.store.sqlalchemy.models import (
    mapping,
)
from search_by_document_texts.infrastructure.store.elasticsearch.connect import (  # noqa
    create_elasticsearch_connect_factory,
)
from search_by_document_texts.presentation.api.v1.dto import (
    DocumentCreate,
    RubricCreate,
)
from search_by_document_texts.infrastructure.store.sqlalchemy.gateways import (
    DocGatewayImpl,
    RubricGatewayImpl,
    CommiterImpl,
)
from search_by_document_texts.infrastructure.store.elasticsearch.gateways import (  # noqa
    DocToSearchGatewayImpl,
)
from search_by_document_texts.сore.handlers import CreateDocHandler


postgres_settings = PostgresSettings()
postgres_settings.host = "localhost"
postgres_settings.port = os.getenv("POSTGRES_HOST_PORT")
es_settings = ElasticsearchSettings()
postgres_settings.host = "localhost"
postgres_settings.port = os.getenv("ELASTIC_HOST_PORT")
mapping()


async def main():
    with open(
        "search_by_document_texts/presentation/cli/posts.csv"
    ) as csvfile:
        async for session in create_session_factory(postgres_settings.url)():
            el_conn = create_elasticsearch_connect_factory(es_settings)()
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            for row in reader:
                text = row["text"]
                created_date = datetime.strptime(
                    row["created_date"], "%Y-%m-%d %H:%M:%S"
                )
                rubrics: list = [
                    RubricCreate(name=r_name.strip("'"))
                    for r_name in row["rubrics"][1:-1].split(", ")
                ]
                doc = DocumentCreate(
                    text=text,
                    rubrics=rubrics,
                    created_date=created_date,
                )

                document_gateway = DocGatewayImpl(session)
                rubric_gateway = RubricGatewayImpl(session)
                doc_to_search_gateway = DocToSearchGatewayImpl(
                    el_conn, es_settings
                )
                commiter = CommiterImpl(session)
                handler = CreateDocHandler(
                    document_gateway,
                    rubric_gateway,
                    doc_to_search_gateway,
                    commiter,
                )
                await handler.execute(doc)


asyncio.run(main())
