from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

def get_blob_service_client(storage_account_name: str) -> BlobServiceClient:
    return BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net/",
        credential=DefaultAzureCredential()
    )

def backup_data(storage_account_name: str, container_name: str, blob_name: str, data: bytes) -> dict:
    """
    Uploads data to Azure Blob Storage for backup.

    :param storage_account_name: The name of the Azure Storage account.
    :param container_name: The name of the Blob container.
    :param blob_name: The name for the blob (file) to create.
    :param data: The data to back up in bytes.
    :return: A dictionary indicating the operation's success or failure.
        The dictionary has the following keys:
        - "status": The status of the backup operation ("success" or "error").
        - "message": A message indicating the result of the backup operation.
        - "details" (optional): Additional details in case of an error.
    :rtype: dict
    :raises Exception: If there is an error during the backup process.
    """
    blob_service_client = get_blob_service_client(storage_account_name)
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client = blob_service_client.get_container_client(container_name).get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        return {"status": "success", "message": "Data backed up successfully."}
    except Exception as e:
        return {"status": "error", "message": "Failed to back up data.", "details": str(e)}

def restore_data(storage_account_name: str, container_name: str, blob_name: str) -> bytes:
    """
    Retrieves data from Azure Blob Storage.

    :param storage_account_name: The name of the Azure storage account.
    :param container_name: The name of the Blob container.
    :param blob_name: The name of the blob (file) to retrieve.
    :return: The data from the blob.
    :raises Exception: If there is an error while restoring the data.
    """
    blob_service_client = get_blob_service_client(storage_account_name)
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        download_stream = blob_client.download_blob()
        return download_stream.readall()
    except Exception as e:
        # In a real application, you might want to handle this differently
        raise Exception(f"Failed to restore data: {str(e)}")
