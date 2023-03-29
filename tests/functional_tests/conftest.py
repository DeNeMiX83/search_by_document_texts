from typing import Callable, AsyncGenerator
import os
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient

from search_by_document_texts.config.settings import Settings
from search_by_document_texts.api.di.stubs import (
    provide_sqlalchemy_session_stub,
)


@pytest.fixture(scope="session")
def client(settings) -> TestClient:
    from search_by_document_texts.api.main import app
    session_factory = create_session_factory(settings.postgres.url)
    app.dependency_overrides.update({
        provide_sqlalchemy_session_stub: session_factory
    })
    return TestClient(app)


@pytest.fixture(scope="session")
def settings() -> Settings:
    with open("deploy/.env.dev") as f:
        for line in f:
            if "=" in line:
                key, value = map(lambda x: x.strip(), line.split("="))
                os.environ[key] = value
    return Settings()


def create_session_factory(
    url: str,
) -> Callable[..., AsyncGenerator[AsyncSession, None]]:
    engine = create_async_engine(url, echo=True, poolclass=NullPool)

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async def session_factory() -> AsyncGenerator[AsyncSession, None]:
        async with async_session() as session:
            yield session

    return session_factory
