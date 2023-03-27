import os
from dataclasses import dataclass, field


@dataclass
class PostgresSettings:
    host: str = field(init=False)
    port: int = field(init=False)
    user: str = field(init=False)
    password: str = field(init=False)
    database: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = os.getenv("POSTGRES_DB")
        self.url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(  # noqa E501
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


@dataclass
class ElasticsearchSettings:
    user: str = field(init=False)
    password: str = field(init=False)
    host: str = field(init=False)
    port: str = field(init=False)
    doc_index: str = field(init=False)

    def __post_init__(self):
        self.user = os.getenv("ELASTICSEARCH_USERNAME")
        self.password = os.getenv("ELASTICSEARCH_PASSWORD")
        self.host = os.getenv("ELASTICSEARCH_HOST")
        self.port = os.getenv("ELASTICSEARCH_PORT")
        self.url = "https://{host}:{port}".format(
            host=self.host,
            port=self.port,
        )
        self.doc_index = os.getenv("DOC_INDEX")


@dataclass
class Settings:
    host: str = field(init=False)
    port: int = field(init=False)
    root_path: str = field(init=False)

    api_url: str = field(init=False)
    docs_url: str = field(init=False)

    postgres: PostgresSettings = field(
        init=False, default_factory=PostgresSettings  # noqa E501
    )

    elasticsearch: ElasticsearchSettings = field(
        init=False, default_factory=ElasticsearchSettings  # noqa E501
    )

    def __post_init__(self):
        self.host = os.getenv("HOST")
        self.port = os.getenv("HOST_BACKEND_PORT")
        self.root_path = os.getenv("ROOT_PATH")
        self.api_url = os.getenv("API_URL")
        self.docs_url = os.getenv("DOCS_URL")
