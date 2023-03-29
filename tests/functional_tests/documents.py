import pytest


class TestDocument:
    async def test_get_all_documents(self, client):
        response = client.get("/api/v1/documents/")
        assert response.status_code == 422

    def test_get_documents_with_text(self, client):
        response = client.get("/api/v1/documents/?text=text")
        assert response.status_code == 200

    def test_create_document(self, client):
        data = {"rubrics": [{"name": "спорт"}], "text": "example text"}
        response = client.post("/api/v1/documents/", json=data)
        assert response.status_code == 200
        
        doc_id = response.json()["id"]
        response = client.delete(f"/api/v1/documents/?doc_id={doc_id}")

    def test_create_document_with_invalid_data(self, client):
        data = {"title": "New Document"}
        response = client.post("/api/v1/documents/", json=data)
        assert response.status_code == 422

    def test_delete_all_documents(self, client):
        response = client.delete("/api/v1/documents/")
        assert response.status_code == 422

    def test_delete_document(self, client):
        data = {"rubrics": [{"name": "спорт"}], "text": "example text"}
        response = client.post("/api/v1/documents/", json=data)
        doc_id = response.json()["id"]

        response = client.delete(f"/api/v1/documents/?doc_id={doc_id}")
        assert response.status_code == 200

    def test_delete_document_with_invalid_id(self, client):
        response = client.delete("/api/v1/documents/?doc_id=invalid_id")
        assert response.status_code == 422
