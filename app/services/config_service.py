import os
import shutil
import subprocess
from fastapi import UploadFile, HTTPException
from tempfile import NamedTemporaryFile, TemporaryDirectory
import logging, zipfile

async def get_terraform_plan(file: UploadFile, environment: str, region: str):
    """
    Deploys Terraform configuration by performing the following steps:
    1. Unpacks the uploaded zip file to a temporary directory.
    2. Validates the presence of the 'provision' directory in the zip file.
    3. Constructs file names based on the environment and region.
    4. Constructs file paths for the backend and variables files.
    5. Ensures both the backend and variables files exist.
    6. Initializes Terraform with the backend configuration.
    7. Generates a Terraform plan using the variables file.
    8. Returns the plan details.

    Args:
        file (UploadFile): The uploaded zip file containing the Terraform configuration.
        environment (str): The environment name.
        region (str): The region name.

    Returns:
        dict: A dictionary containing the Terraform plan details.

    Raises:
        FileNotFoundError: If the 'provision' directory is not found in the zip file,
            or if either the backend or variables files are missing.
    """
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        zip_path = temp_file.name
    
    try:
        with TemporaryDirectory() as temp_dir:
            # Attempt to unpack the zip file
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except zipfile.BadZipFile:
                logging.error("Uploaded file is not a zip archive or is corrupted.")
                raise HTTPException(status_code=400, detail="Invalid zip file.")
            finally:
                os.remove(zip_path)  # Clean up the zip file

            provision_path = os.path.join(temp_dir, "provision")
            if not os.path.exists(provision_path):
                logging.error("No 'provision' directory found in the zip file.")
                raise FileNotFoundError("No 'provision' directory found in the zip file.")
            
            # Construct file names based on environment and region
            backend_file_name = f"backend.{environment}01.{region}.conf"
            variables_file_name = f"variables.{environment}01.{region}.tfvars"

            # Construct file paths
            backend_file_path = os.path.join(temp_dir, "config", backend_file_name)
            variables_file_path = os.path.join(temp_dir, "variables", variables_file_name)

            # Ensure both the backend and variables files exist
            if not os.path.exists(backend_file_path) or not os.path.exists(variables_file_path):
                logging.error("Both the backend and variables files must exist.")
                raise FileNotFoundError("Both the backend and variables files must exist.")
            
            # Initialize Terraform with backend configuration
            subprocess.run(["terraform", "init", "-backend-config=" + backend_file_path], check=True, cwd=provision_path)

            # Generate a Terraform plan
            plan_output = subprocess.run(["terraform", "plan", "-var-file=" + variables_file_path, "-out=plan.tfplan"], check=True, cwd=provision_path, capture_output=True, text=True)
            plan_details = plan_output.stdout

            return {"plan": plan_details}
    except Exception as e:
        logging.error(f"An error occurred during Terraform deployment: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during Terraform deployment.")