# Project Percival
This project is a web interface for managing actions on Azure DevOps and Azure. It uses Streamlit for the web interface and FastAPI for the backend API.

## Features
1. Trigger Deployment: This feature allows you to trigger a deployment to an Azure DevOps pipeline. You just need to provide the pipeline ID and the branch name.

2. Fetch Storage Metrics: This feature allows you to fetch storage metrics from an Azure Storage Account. You need to provide the subscription ID, resource group name, and storage account name.

3. Deploy Terraform Infrastructure: This features allows you to deploy terraform infrastructure based on a specific folder structure. 

4. Backup and Restore: This feature allows you to backup and restore any file to/from an Azure storage account

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.8 or higher
- Docker
- Docker Compose

### Installation
1. Clone the repository:
2. Navigate to the project directory:
3. Install the required Python packages:
4. Build the Docker images:
5. Start the services:
6. The Streamlit web interface should now be accessible at http://localhost:8501.

# Usage
Trigger Deployment: Enter the pipeline ID and the branch name in the respective text input fields and click the 'Trigger Deployment' button.
![Alt text](images/pipeline_deployment.png?raw=true)

Fetch Storage Metrics: Enter the subscription ID, resource group name, and storage account name in the respective text input fields and click the 'Fetch Metrics' button.
![Alt text](images/insights.png?raw=true)

Terraform Infrastructure Deployment: Upload a zip file containing terraform IaC following a specific file structure 

![Alt text](images/iac_structure.png?raw=true)
![Alt text](images/terraform_deployment.png?raw=true)

Backup and Restore: For backup, enter storage account name and container name. Upload the file(s) that you want to backup. For restore, enter the name of the blob along with storage account name and container name.
![Alt text](images/backup.png?raw=true)
![Alt text](images/restore.png?raw=true)
# Running the tests
To run the tests, navigate to the project directory and run the following command:

`pytest` or `pytest path/to/test_deploy_terraform.py`

## Built With
- Streamlit - The web framework used
- FastAPI - The backend API framework used
- Azure - Cloud platform for infrastructure
- GitHub Actions - CI/CD deployment
# Contributing
Contributions are welcome. Please submit a Pull Request.

