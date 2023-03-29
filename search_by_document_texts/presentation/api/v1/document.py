from fastapi import APIRouter, Depends, status, Query

from search_by_document_texts.сore.handlers import (
    CreateDocHandler,
    SearchDocByQuery,
    DeleteDocHandler,
)
from search_by_document_texts.presentation.api.di.stubs import (
    provide_create_doc_handler_stub,
    provide_search_doc_handler_stub,
    provide_delete_doc_handler_stub,
)
from .dto import Document, DocumentCreate, DocumentDelete, QueryForSearchDoc

router = APIRouter()


@router.post(path="/", status_code=status.HTTP_200_OK)
async def create_document(
    document: DocumentCreate,
    handler: CreateDocHandler = Depends(provide_create_doc_handler_stub),
):
    doc_create = await handler.execute(document)
    doc_create = Document.from_entity(doc_create)
    return doc_create


@router.get(path="/", status_code=status.HTTP_200_OK)
async def search_documents(
    text: str = Query(...),
    handler: SearchDocByQuery = Depends(provide_search_doc_handler_stub),
):
    docs = await handler.execute(QueryForSearchDoc(text=text))
    return docs


@router.delete(path="/", status_code=status.HTTP_200_OK)
async def delete_document(
    doc_id: int = Query(...),
    handler: DeleteDocHandler = Depends(provide_delete_doc_handler_stub),
):
    await handler.execute(DocumentDelete(id=doc_id))
    return {"message": "Document deleted successfully"}
