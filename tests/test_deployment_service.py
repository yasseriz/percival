# tests/test_deployment_service.py

import pytest
from app.services.deployment_service import trigger_pipeline_deployments
from httpx import Response
from unittest.mock import Mock

@pytest.fixture
def mock_response_success():
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"some": "response"}
    return mock_response

@pytest.fixture
def mock_response_fail():
    mock_response = Mock(spec=Response)
    mock_response.status_code = 400
    mock_response.text = "Failed due to bad request"
    return mock_response

def test_trigger_pipeline_deployments_success(mocker, mock_response_success):
    mocker.patch("httpx.post", return_value=mock_response_success)
    result = trigger_pipeline_deployments("1", "main")
    assert result == {"status": "success", "message": "Deployment triggered successfully"}

def test_trigger_pipeline_deployments_fail(mocker, mock_response_fail):
    mocker.patch("httpx.post", return_value=mock_response_fail)
    result = trigger_pipeline_deployments("1", "main")
    assert result == {"status": "error", "message": "Deployment failed to trigger", "details": "Failed due to bad request"}

def test_trigger_pipeline_deployments_unexpected_status_code(mocker):
    unexpected_status_mock_response = Mock(spec=Response)
    unexpected_status_mock_response.status_code = 500
    unexpected_status_mock_response.text = "Server error"
    mocker.patch("httpx.post", return_value=unexpected_status_mock_response)
    result = trigger_pipeline_deployments("1", "main")
    assert result["status"] == "error"
    assert "Server error" in result["details"]
