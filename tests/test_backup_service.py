import pytest
from app.services.backup_service import backup_data, restore_data, get_blob_service_client
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
from azure.storage.blob import BlobServiceClient
from unittest.mock import Mock

@pytest.fixture
def mock_blob_service_client(mocker):
    mock_client = Mock(spec=BlobServiceClient)
    mocker.patch('app.services.backup_service.get_blob_service_client', return_value=mock_client)
    return mock_client

def test_get_blob_service_client(mocker):
    mocker.patch('azure.identity.DefaultAzureCredential', return_value=Mock())
    client = get_blob_service_client("testaccount")
    assert client is not None
    assert "testaccount.blob.core.windows.net" in str(client.url)

def test_backup_data_success(mock_blob_service_client):
    mock_blob_client = Mock()
    mock_blob_client.upload_blob.return_value = None
    mock_blob_service = mock_blob_service_client.get_blob_client
    mock_blob_service.return_value = mock_blob_client

    result = backup_data("testaccount", "test-container", "test-blob", b"test data")
    assert result["status"] == "success"

def test_restore_data_success(mock_blob_service_client):
    expected_data = b"test data"
    mock_blob_client = Mock()
    mock_blob_client.download_blob().readall.return_value = expected_data
    mock_blob_service = mock_blob_service_client.get_blob_client
    mock_blob_service.return_value = mock_blob_client

    data = restore_data("testaccount", "test-container", "test-blob")
    assert data == expected_data


def test_backup_data_failure(mock_blob_service_client):
    mock_blob_client = Mock()
    mock_blob_client.upload_blob.side_effect = HttpResponseError(message="Network error")
    mock_blob_service = mock_blob_service_client.get_blob_client
    mock_blob_service.return_value = mock_blob_client

    result = backup_data("testaccount", "test-container", "test-blob", b"test data")
    assert result["status"] == "error"
    assert "Network error" in result["message"]

def test_restore_data_not_found_failure(mock_blob_service_client):
    mock_blob_client = Mock()
    mock_blob_client.download_blob.side_effect = ResourceNotFoundError(message="Blob not found")
    mock_blob_service = mock_blob_service_client.get_blob_client
    mock_blob_service.return_value = mock_blob_client

    with pytest.raises(Exception) as excinfo:
        restore_data("testaccount", "test-container", "test-blob")
    assert "Blob not found" in str(excinfo.value)

def test_restore_data_http_failure(mock_blob_service_client, mocker):
    mock_blob_client = Mock()
    # Simulate a different failure, such as an HttpResponseError
    mock_blob_client.download_blob().readall.side_effect = HttpResponseError(message="HTTP error")
    mock_blob_service = mock_blob_service_client.get_blob_client
    mock_blob_service.return_value = mock_blob_client

    with pytest.raises(Exception) as excinfo:
        restore_data("testaccount", "test-container", "test-blob")
    assert "HTTP error" in str(excinfo.value)