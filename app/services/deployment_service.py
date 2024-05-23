import httpx
import os
import base64
import logging
from app.utils.env_loader import get_config_value
logger = logging.getLogger(__name__)

pat = get_config_value("PAT")
logger.info(f"Retrieved PAT")
encoded_pat = base64.b64encode(f":{pat}".encode("ascii")).decode("ascii")

def trigger_pipeline_deployments(pipeline_id: str, branch: str = "main"):
    """
    Triggers a deployment to an azure devops pipeline 
    :param pipeline_id: The id of the pipeline to trigger
    :param branch: The branch to trigger the deployment for
    """
    # pipeline_url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}/runs?api-version=7.0"
    pipeline_url = f"https://dev.azure.com/service-yasser/Freelance/_apis/pipelines/{pipeline_id}/runs?api-version=7.0-preview.1"
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_pat}"
}
    pipeline_body = {
        "resources": {
            "repositories": {
                "self": {
                    "refName": branch
                }
            }
        }
    }
    logger.info(f"Triggering deployment for pipeline: {pipeline_id}")
    response = httpx.post(pipeline_url, json=pipeline_body, headers=headers, follow_redirects=False)
    logger.info(f"Interpreting command: {response.status_code}")
    if response.status_code == 200 or response.status_code == 201:
        return {"status": "success", "message": "Deployment triggered successfully"}
    elif response.status_code == 404:
        return {"status": "error", "message": "Pipeline not found", "details": response.text}
    else:
        return {"status": "error", "message": "Deployment failed to trigger", "details": response.text}