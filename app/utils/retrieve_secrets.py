from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import logging
import os
logger = logging.getLogger(__name__)

def to_keyvault_name(env_var_name):
    """
    Convert an environment variable name to a Key Vault secret name.
    Example: 'AZURE_CLIENT_ID' -> 'azureClientId'
    """
    logger.info(f"Converting {env_var_name} to Key Vault name")
    print(f"Converting {env_var_name} to Key Vault name")
    parts = env_var_name.lower().split('_')
    return parts[0] + ''.join(part.capitalize() for part in parts[1:])

def from_keyvault_name(kv_name):
    """
    Convert a Key Vault secret name back to an environment variable name.
    Example: 'azureClientId' -> 'AZURE_CLIENT_ID'
    """
    return ''.join('_' + c if c.isupper() else c for c in kv_name).upper()


def get_secret(secret_name: str):
    """
    Retrieves the value of a secret from Azure Key Vault, expecting and returning the local naming convention for the secret name.

    Args:
        secret_name (str): The name of the secret to retrieve, in local .env format.

    Returns:
        dict: A dictionary with the original environment variable name as the key and the secret's value.

    Raises:
        AzureError: If there is an error retrieving the secret.
    """
    # Convert to Key Vault compatible name
    kv_secret_name = to_keyvault_name(secret_name)
    print(f"Retrieving secret {kv_secret_name} from Azure Key Vault")
    keyvault_url = "https://pptst01atmkvtsea01.vault.azure.net/"
    credential = ManagedIdentityCredential(client_id="58246e13-0a2d-4d1a-89f0-19d9c18ca469")
    client = SecretClient(vault_url=keyvault_url, credential=credential)
    
    try:
        secret = client.get_secret(kv_secret_name).value
        logger.info(f"Retrieved secret {secret_name} from Azure Key Vault")
        print(f"Retrieved secret {secret_name} from Azure Key Vault")
        # Set the secret as an environment variable in the required format
        os.environ[secret_name] = secret
        return secret
    except Exception as e:
        raise Exception(f"Failed to retrieve secret {secret_name} from Azure Key Vault: {str(e)}")
