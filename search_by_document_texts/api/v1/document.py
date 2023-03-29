from fastapi import APIRouter, Depends, status, Query

from search_by_document_texts.сore.handlers import (
    CreateDocHandler,
    SearchDocByQuery,
    DeleteDocHandler,
)
from search_by_document_texts.api.di.stubs import (
    provide_create_doc_handler_stub,
    provide_search_doc_handler_stub,
    provide_delete_doc_handler_stub,
)
from .dto import DocumentCreate, QueryForSearchDoc, DocumentDelete

router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def create_document(
    document: DocumentCreate,
    handler: CreateDocHandler = Depends(provide_create_doc_handler_stub),
):
    await handler.execute(document)
    return {"message": "Document created successfully"}


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def search_documents(
    text: str = Query(None),
    handler: SearchDocByQuery = Depends(provide_search_doc_handler_stub),
):
    docs = await handler.execute(QueryForSearchDoc(text=text))
    return docs


@router.delete(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def delete_document(
    doc_id: str = Query(None),
    handler: DeleteDocHandler = Depends(provide_delete_doc_handler_stub),
):
    await handler.execute(DocumentDelete(id=doc_id))
    return {"message": "Document deleted successfully"}
