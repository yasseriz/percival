from azure.identity import ManagedIdentityCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.utils.env_loader import get_config_value

load_dotenv()

def get_storage_account_utilization(subscription_id: str, resource_group_name: str, storage_account_name: str):
    client_id_secret = get_config_value("AZURE_CLIENT_ID")
    monitor_client = MonitorManagementClient(
        ManagedIdentityCredential(client_id=client_id_secret),
        subscription_id
    )
    resource_uri = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}"
    timespan = f"{(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')}/{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}"
    interval = "PT1H"

    metrics_data = monitor_client.metrics.list(resource_uri=resource_uri, timespan=timespan, interval=interval, metricnames="Transactions,UsedCapacity,Egress,Ingress", aggregation="Total")
    return metrics_data.as_dict()

# def get_storage_cost(subscription_id: str, resource_group_name: str, storage_account_name: str):
#     cost_client = CostManagementClient(
#         DefaultAzureCredential(),
#         subscription_id
#     )
#     scope = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}"
#     query = {
#         "type": "Usage",
#         "timeframe": "TheLastMonth",
#         "dataset": {
#             "granularity": "Daily",
#             "aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}},
#         },
#     }
#     cost_data = cost_client.query.usage(scope, query)
#     return cost_data.as_dict()