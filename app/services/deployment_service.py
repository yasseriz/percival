import httpx
import os
import base64

pat = os.getenv("PAT")
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
    response = httpx.post(pipeline_url, json=pipeline_body, headers=headers, follow_redirects=False)

    if response.status_code in (200,201):
        return {"status": "success", "message": "Deployment triggered successfully"}
    else:
        return {"status": "error", "message": "Deployment failed to trigger", "details": response.text} 