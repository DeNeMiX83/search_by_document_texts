from elasticsearch import AsyncElasticsearch
from search_by_document_texts.config.settings import ElasticsearchSettings


class Gateway:
    def __init__(
        self, connect: AsyncElasticsearch, el_settings: ElasticsearchSettings
    ):
        self._connect = connect
        self._el_settings = el_settings
