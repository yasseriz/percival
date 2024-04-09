import pytest
from httpx import AsyncClient
from unittest.mock import patch, Mock
from app.main import app  # Import your FastAPI app instance

# Mock BlobServiceClient for all tests in this file
@pytest.fixture(autouse=True)
def mock_blob_service_client(monkeypatch):
    mock_client = Mock()
    # Mock methods used in your backup_service.py
    monkeypatch.setattr("app.services.backup_service.BlobServiceClient", Mock(return_value=mock_client))
    mock_blob_client = Mock()
    mock_blob_client.upload_blob.return_value = Mock()
    mock_blob_client.download_blob().readall.return_value = b"fake data"
    mock_client.get_blob_client.return_value = mock_blob_client
    mock_client.get_container_client().get_blob_client.return_value = mock_blob_client
    return mock_client

@pytest.mark.asyncio
async def test_backup_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/upload-files",
            data={"storage_account_name": "testaccount", "container_name": "testcontainer"},
            files={"files": ("testfile.txt", b"Hello, world!")}
        )
    assert response.status_code == 200
    assert "success" in response.text

@pytest.mark.asyncio
async def test_backup_failure():
    # Ensure that we're patching the method used in the actual backup operation
    with patch("app.services.backup_service.BlobServiceClient.get_blob_client") as mock_get_blob_client:
        mock_blob_client = Mock()
        # Simulating an upload failure
        mock_blob_client.upload_blob.side_effect = Exception("Upload failed")
        mock_get_blob_client.return_value = mock_blob_client

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/upload-files/",
                data={"storage_account_name": "failaccount", "container_name": "failcontainer"},
                files={"files": ("failfile.txt", b"Bad data")}
            )
    
    # Check for the expected 500 error status code
    assert response.status_code == 500, "Expected a 500 error status code but received {0}".format(response.status_code)