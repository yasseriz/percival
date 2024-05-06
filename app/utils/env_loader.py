import os
from dotenv import load_dotenv
from app.utils.retrieve_secrets import get_secret

def get_config_value(name):
    """
    Get configuration value either from environment or Azure Key Vault.
    If `ENV` is set to "local", it will read from .env file.
    Otherwise, it will use Azure Key Vault via the `get_secret` function.
    """
    if os.getenv("ENV") == "local":
        # Load variables from .env file
        load_dotenv()
        return os.getenv(name)
    else:
        # Get from Azure Key Vault
        return get_secret(name)
