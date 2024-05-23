import streamlit as st
import requests
import base64

st.title('Welcome to the Web Interface')

# User input for pipeline id and branch name
pipeline_id = st.text_input("Enter the pipeline ID")
branch = st.text_input("Enter the branch name", value="main")

if st.button('Trigger Deployment'):
    # Prepare the payload
    payload = {
        'pipeline_id': pipeline_id,
        'branch': branch
    }
    response = requests.post('http://fastapi:8000/deploy', json=payload)
    # Post the request to the FASTAPI endpoint
    if response.status_code == 200:
        st.success('Deployment triggered successfully')
    else:
        st.error('Deployment failed to trigger')

st.title('Azure Storage Account Insights')
st.header('Get Storage Metrics Utilization')
subscription_id = st.text_input("Enter the subscription ID")
resource_group_name = st.text_input("Enter the resource group name")
storage_account_name = st.text_input("Enter the storage account name")

if st.button('Fetch Metrics'):
    # Construct the URL
    url = f"http://fastapi:8000/storage-metrics/{subscription_id}/{resource_group_name}/{storage_account_name}"
    response = requests.get(url)
    if response.status_code == 200:
        metrics = response.json()
        st.success('Metrics fetched successfully')
        st.json(metrics)
    else:
        st.error(f"Failed to fetch metrics: {response.text}")

st.title('Azure Blob Storage Backup and Restore')
st.header('Backup Data to Azure Blob Storage')

storage_account_name_backup = st.text_input("Enter the storage account name to backup to")
container_name_backup = st.text_input("Enter the container name")
uploaded_files = st.file_uploader("Choose a file to upload", accept_multiple_files=True)

if st.button('Backup files'):
    if uploaded_files and storage_account_name_backup and container_name_backup:
        for uploaded_file in uploaded_files:
            files = {
                'files': (uploaded_file.name, uploaded_file, uploaded_file.type),
                'storage_account_name': (None, storage_account_name_backup),
                'container_name': (None, container_name_backup)
            }
            response = requests.post(
                f'http://fastapi:8000/upload-files',
                files=files
            )
            if response.status_code == 200:
                st.success(f"File {uploaded_file.name} backed up successfully")
                st.json(response.json())
            else:
                st.error(f"Failed to back up file {uploaded_file.name}: {response.text}")

    else:
        st.warning("Please fill in all fields and upload at least one file.")

st.header('Restore Data from Azure Blob Storage')
storage_account_name_restore = st.text_input('Enter Storage Account Name for Restore', key='storage_account_restore')
container_name_restore = st.text_input('Enter Blob Container Name for Restore', key='container_restore')
blob_name_restore = st.text_input('Enter Blob Name to Restore', key='blob_restore')

if st.button('Restore File'):
    if storage_account_name_restore and container_name_restore and blob_name_restore:
        restore_payload = {
            "storage_account_name": storage_account_name_restore.strip(),
            "container_name": container_name_restore.strip(),
            "blob_name": blob_name_restore.strip()
        }
        restore_url = 'http://fastapi:8000/restore'
        response = requests.post(restore_url, json=restore_payload)
        if response.status_code == 200:
            blob_data = response.content
            b64 = base64.b64encode(blob_data).decode()
            href = f'<a href="data:file/octet-stream;base64,{b64}" download="{blob_name_restore}">Download {blob_name_restore}</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success('File restored successfully. Click the link above to download it.')
        else:
            st.error(f"Failed to restore file: {response.text}")
    else:
        st.warning("Please fill in all fields to restore a file.")

st.title('Terraform Deployment Plan')
st.header('Plan Terraform Infrastructure')

environment = st.selectbox("Select Environment", ['tst', 'stg', 'prod'])
region = st.selectbox("Select Region", ['sea', 'wu3', 'cac'])
uploaded_zip = st.file_uploader("Upload Terraform ZIP file", type=["zip"])

if st.button("Generate Terraform Plan"):
    if uploaded_zip and environment and region:
        files = {'file': (uploaded_zip.name, uploaded_zip, 'application/zip')}
        response = requests.post(
            f'http://fastapi:8000/deploy-terraform?environment={environment}&region={region}',
            files=files
        )
        if response.status_code == 200:
            st.success("Terraform plan generated successfully.")
            st.json(response.json())  # Display the plan
        else:
            st.error(f"Failed to generate plan: {response.text}")
    else:
        st.warning("Please upload a ZIP file and select environment and region.")

st.header('Apply Terraform Plan')
provision_path = st.text_input("Enter the provision path")

if st.button("Apply Terraform Plan"):
    if provision_path:
        response = requests.post(
            f'http://fastapi:8000/apply-terraform-plan',
            json={"provision_path": provision_path}
        )
        if response.status_code == 200:
            st.success(response.json()['message'])
        else:
            st.error(f"Failed to apply plan: {response.text}")
    else:
        st.warning("Please specify the provision path.")

