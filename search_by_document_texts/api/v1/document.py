from fastapi import APIRouter, Depends, status, Query

from search_by_document_texts.сore.handlers import (
    CreateDocHandler,
    SearchDocByQuery,
)
from search_by_document_texts.api.di.stubs import (
    provide_create_doc_handler_stub,
    provide_search_doc_handler_stub,
)
from .dto import Document, QueryForSearchDoc

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
    return {"message": "Document created successfully"}


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def search_documents(
    query: str = Query(None),
    handler: SearchDocByQuery = Depends(provide_search_doc_handler_stub),
):
    docs = await handler.execute(
        QueryForSearchDoc(text=query)
    )
    return docs
