from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def get_secret(secret_name: str):
    """
    Retrieves the value of a secret from Azure Key Vault.

    Args:
        secret_name (str): The name of the secret to retrieve.

    Returns:
        str: The value of the secret.

    Raises:
        AzureError: If there is an error retrieving the secret.
    """
    keyvault_url = os.getenv("KEYVAULT_URL")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=keyvault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value