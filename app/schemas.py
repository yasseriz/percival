from pydantic import BaseModel

class Deployment(BaseModel):
    pipeline_id: str
    branch: str

class Restore(BaseModel):
    storage_account_name: str
    container_name: str
    blob_name: str