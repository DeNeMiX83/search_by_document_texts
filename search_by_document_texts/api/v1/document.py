from fastapi import APIRouter, Depends, status

from search_by_document_texts.сore.handlers import CreateDocHandler
from search_by_document_texts.api.di.stubs import (
    provide_create_doc_handler_stub,
)
from .dto import Document

router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def create_document(
    document: Document,
    handler: CreateDocHandler = Depends(provide_create_doc_handler_stub),
):
    await handler.execute(document)
    return {'message': 'Document created successfully'}
