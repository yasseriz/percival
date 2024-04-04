from pydantic import BaseModel

class Deployment(BaseModel):
    pipeline_id: str
    branch: str

class ResponseModel(BaseModel):
    result: str
    status_code: int