import pytest
from app.services.deployment_service import trigger_pipeline_deployments

def test_trigger_pipeline_deployments_success():
    assert trigger_pipeline_deployments("1") == True

def test_trigger_pipeline_deployments_failure():
    assert trigger_pipeline_deployments("") == False