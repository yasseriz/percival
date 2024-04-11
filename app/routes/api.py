from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.services.deployment_service import trigger_pipeline_deployments
from app.services.backup_service import backup_data, restore_data
from app.services.insights_service import get_storage_account_utilization, get_storage_cost
from app.schemas import Deployment, Restore
from typing import List

router = APIRouter()

@router.post("/deploy", tags=["deployments"])
async def deploy(request: Deployment):
    """
    Triggers a deployment to an azure devops pipeline
    :param pipeline_id: The ID of the pipeline to trigger the deployment for
    :param branch: The branch to trigger the deployment for
    """
    return trigger_pipeline_deployments(request.pipeline_id, request.branch)

@router.post("/upload-files", tags=["backup"])
async def backup(storage_account_name: str = Form(...), container_name: str = Form(...), files: List[UploadFile] = File(...)):
    """
    Triggers a backup of data to Azure Blob Storage

    :param storage_account_name: The name of the Azure Storage account
    :param container_name: The name of the Blob container
    :param files: List of files to be uploaded
    :type files: List[UploadFile]
    :return: List of upload results
    :rtype: List[Dict[str, Any]]
    :raises HTTPException: If there is an error during the backup process
    """
    upload_results = []
    for file in files:
        try:
            file_content = await file.read()
            result = backup_data(storage_account_name, container_name, file.filename, file_content)
            upload_results.append(result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await file.close()
    return upload_results

@router.post("/restore", tags=["restore"])
async def restore(request: Restore):
    """
    Triggers a restore of data from Azure Blob Storage
    :param storage_account_name: The name of the Azure storage account
    :param container_name: The name of the Blob container
    :param blob_name: The name of the blob (file) to retrieve
    """
    return restore_data(request.storage_account_name, request.container_name, request.blob_name)

@router.get("/storage-metrics/{subscription_id}/{resource_group_name}/{storage_account_name}", tags=["insights"])
async def storage_metrics(subscription_id: str, resource_group_name: str, storage_account_name: str):
    """
    Retrieves metrics for a storage account
    :param subscription_id: The subscription ID
    :param resource_group_name: The resource group name
    :param storage_account_name: The storage account name
    """
    return get_storage_account_utilization(subscription_id, resource_group_name, storage_account_name)

@router.get("/cost-management/{subscription_id}/{resource_group_name}/{storage_account_name}", tags=["insights"])
async def storage_cost(subscription_id: str, resource_group_name: str, storage_account_name: str):
    """
    Retrieves cost management data for a storage account
    :param subscription_id: The subscription ID
    :param resource_group_name: The resource group name
    :param storage_account_name: The storage account name
    """
    return get_storage_cost(subscription_id, resource_group_name, storage_account_name)