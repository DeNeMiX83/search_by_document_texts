from fastapi import APIRouter
from search_by_document_texts.presentation.api.v1 import document
from search_by_document_texts.config.settings import Settings

settings = Settings()

router = APIRouter(prefix=settings.api_url)
router.include_router(document.router, prefix="/documents", tags=["documents"])
