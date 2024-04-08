from fastapi import APIRouter
from app.services.deployment_service import trigger_pipeline_deployments
from app.services.backup_service import backup_data, restore_data
from app.schemas import Deployment, Backup, Restore

router = APIRouter()

@router.post("/deploy", tags=["deployments"])
async def deploy(request: Deployment):
    """
    Triggers a deployment to an azure devops pipeline
    :param pipeline_id: The ID of the pipeline to trigger the deployment for
    :param branch: The branch to trigger the deployment for
    """
    return trigger_pipeline_deployments(request.pipeline_id, request.branch)

@router.post("/backup", tags=["backup"])
async def backup(request: Backup):
    """
    Triggers a backup of data to Azure Blob Storage
    :param storage_account_name: The name of the Azure Storage account
    :param container_name: The name of the Blob container
    :param blob_name: The name of the blob (file) to create
    :param data: The data to back up in bytes
    """
    return backup_data(request.storage_account_name, request.container_name, request.blob_name, request.data)

@router.post("/restore", tags=["restore"])
async def restore(request: Restore):
    """
    Triggers a restore of data from Azure Blob Storage
    :param storage_account_name: The name of the Azure storage account
    :param container_name: The name of the Blob container
    :param blob_name: The name of the blob (file) to retrieve
    """
    return restore_data(request.storage_account_name, request.container_name, request.blob_name)