import pytest
from unittest.mock import patch, Mock
from app.services.insights_service import get_storage_account_utilization#, get_storage_cost

@pytest.fixture
def mock_monitor_client():
    with patch('azure.mgmt.monitor.MonitorManagementClient') as MockClass:
        yield MockClass()

# @pytest.fixture
# def mock_cost_client():
#     with patch('azure.mgmt.costmanagement.CostManagementClient') as MockClass:
#         yield MockClass()

@patch('app.services.insights_service.MonitorManagementClient')
def test_get_storage_account_utilization(mock_monitor_client):
    # Set up mock response
    mock_response = Mock()
    mock_response.as_dict.return_value = {"value": "mocked data"}
    mock_monitor_client.return_value.metrics.list.return_value = mock_response

    # Call the function
    result = get_storage_account_utilization("sub_id", "rg_name", "storage_account")

    # Assertions
    mock_monitor_client.return_value.metrics.list.assert_called_once()
    assert result == {"value": "mocked data"}

# def test_get_storage_cost(mock_cost_client):
#     # Set up mock response
#     mock_response = Mock()
#     mock_response.as_dict.return_value = {"value": "mocked cost data"}
#     mock_cost_client.return_value.query.usage.return_value = mock_response

#     # Call the function
#     result = get_storage_cost("sub_id", "rg_name", "storage_account")

#     # Assertions
#     mock_cost_client.return_value.query.usage.assert_called_once()
#     assert result == {"value": "mocked cost data"}
