from fastapi import APIRouter
from app.services.deployment_service import trigger_pipeline_deployments
from app.schemas import Deployment

router = APIRouter()

@router.get("/deploy", response_model=Deployment, tags=["deployments"])
async def deploy(pipeline_id: str, branch: str = "main"):
    """
    Triggers a deployment to an azure devops pipeline
    :param pipeline_id: The ID of the pipeline to trigger the deployment for
    :param branch: The branch to trigger the deployment for
    """
    return trigger_pipeline_deployments(pipeline_id, branch)