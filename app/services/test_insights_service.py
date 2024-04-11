import pytest
from app.services.insights_service import get_storage_account_utilization
from azure.monitor.query import MetricsQueryResult
from unittest.mock import Mock

@pytest.fixture
def mock_metrics_data():
    mock_metrics_data = Mock(spec=MetricsQueryResult)
    mock_metrics_data.as_dict.return_value = {
        "Transactions": [10, 20, 30],
        "UsedCapacity": [100, 200, 300],
        "Egress": [50, 60, 70],
        "Ingress": [80, 90, 100]
    }
    return mock_metrics_data

# def test_get_storage_account_utilization(mock_metrics_data):
#     # Mock the MonitorManagementClient and its metrics.list method
#     mock_monitor_client = Mock()
#     mock_monitor_client.metrics.list.return_value = mock_metrics_data

#     # Mock the DefaultAzureCredential
#     mock_default_credential = Mock()

#     # Patch the necessary modules with the mocks
#     with patch("app.services.insights_service.MonitorManagementClient", return_value=mock_monitor_client), \
#          patch("app.services.insights_service.DefaultAzureCredential", return_value=mock_default_credential):
        
#         # Call the function under test
#         result = get_storage_account_utilization("subscription_id", "resource_group_name", "storage_account_name")

#         # Assert the result
#         assert result == {
#             "Transactions": [10, 20, 30],
#             "UsedCapacity": [100, 200, 300],
#             "Egress": [50, 60, 70],
#             "Ingress": [80, 90, 100]
#         }