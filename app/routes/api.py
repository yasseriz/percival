from fastapi import APIRouter
from app.services.deployment_service import trigger_pipeline_deployments
from app.schemas import Deployment

router = APIRouter()

@router.post("/deploy", tags=["deployments"])
async def deploy(request: Deployment):
    """
    Triggers a deployment to an azure devops pipeline
    :param pipeline_id: The ID of the pipeline to trigger the deployment for
    :param branch: The branch to trigger the deployment for
    """
    return trigger_pipeline_deployments(request.pipeline_id, request.branch)