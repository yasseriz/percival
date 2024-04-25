from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query, Body
from app.services.deployment_service import trigger_pipeline_deployments
from app.services.backup_service import backup_data, restore_data
from app.services.insights_service import get_storage_account_utilization#, get_storage_cost
from app.services.config_service import get_terraform_plan
from app.services.nlp_service import CommandInterpreter
from app.utils.command_parser import parse_command
from app.schemas import Deployment, Restore, UserInput
from typing import List
import subprocess

router = APIRouter()
# interpreter = CommandInterpreter('')

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

@router.post("/deploy-terraform", tags=["deployments"])
async def deploy_terraform(file: UploadFile = File(...), environment: str = Query(..., regex="^(tst|stg|prod)$"), region: str = Query(..., regex="^(sea)$")):
    """
    Triggers a deployment of Terraform files to Azure

    :param file: List of Terraform files to deploy
    :type file: List[UploadFile]
    :param environment: The environment to deploy the files to (tst, stg, prod)
    :type environment: str
    :param region: The region to deploy the files to (sea)
    :type region: str
    :return: The result of the deployment
    :rtype: Any
    :raises HTTPException: If the file is not a zip file
    """
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only zip files are supported")
    return await get_terraform_plan(file, environment, region)

@router.post("/apply-terraform-plan", tags=["deployments"])
async def apply_terraform_plan(provision_path: str):
    """
    Apply a Terraform plan to provision infrastructure.

    Args:
        provision_path (str): The path to the directory containing the Terraform files.

    Returns:
        dict: A dictionary with a success message indicating that the Terraform plan was applied successfully.
    """
    subprocess.run(["terraform", "apply", "plan.tfplan"], check=True, cwd=provision_path)
    return {"message": "Terraform plan applied successfully"}

@router.post("/execute-command", tags=["nlp"])
async def execute_command(user_input: UserInput):
    action = interpreter.interpret_command(user_input)
    if action is None:
        raise HTTPException(status_code=500, detail="Failed to interpret command or no output from interpreter")
    try:
        command_details = parse_command(action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if command_details["type"] == "deploy":
        return trigger_pipeline_deployments(command_details["pipeline_id"], command_details["branch"])

    elif command_details["type"] == "backup":
        # Instead of directly performing the backup, instruct the user to upload files
        return {"message": "Please upload your files for backup using the /upload-files-for-backup endpoint.", 
                "details": {"storage_account_name": command_details['storage_account_name'], 
                            "container_name": command_details['container_name']}}
    elif command_details["type"] == "restore":
        return restore_data(command_details["storage_account_name"], command_details["container_name"], command_details["blob_name"])
    elif command_details["type"] == "metrics":
        return get_storage_account_utilization(command_details["subscription_id"], command_details["resource_group_name"], command_details["storage_account_name"])
    elif command_details["type"] == "deploy-terraform":
        return {"message": "Please upload your Terraform files for deployment using the /deploy-terraform endpoint.", "details": {"environment": command_details["environment"], "region": command_details["region"]}}
    elif command_details["type"] == "apply-terraform-plan":
        return apply_terraform_plan(command_details["provision_path"])
    else:
        raise HTTPException(status_code=404, detail="Action not found")