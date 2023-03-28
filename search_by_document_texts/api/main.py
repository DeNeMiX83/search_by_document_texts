from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from search_by_document_texts.api.di.di import setup_di

from search_by_document_texts.api.routes import router

from search_by_document_texts.infrastructure.store.sqlalchemy.models import (
    mapping as sqlalchemy_mapping,
)
from search_by_document_texts.infrastructure.store.elasticsearch.register_index import (  # noqa
    mapping as elasticsearch_mapping,
)
from search_by_document_texts.config.settings import Settings


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Document search API",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app() -> FastAPI:
    settings = Settings()

    app = FastAPI(
        root_path=settings.root_path,
        docs_url=settings.api_url + settings.docs_url,
        port=settings.port
    )
    setup_di(app, settings)
    sqlalchemy_mapping()

    app.include_router(router)
    app.openapi = custom_openapi

    return app


app = create_app()
