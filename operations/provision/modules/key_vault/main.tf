terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.98.0"
    }
  }
}

data "azurerm_client_config" "current" {}

data "azurerm_managed_application_definition" "percival" {
  name                = var.managed_app_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_key_vault" "keyvault" {
  name                        = var.key_vault_name
  location                    = var.key_vault_location
  resource_group_name         = var.resource_group_name
  enabled_for_disk_encryption = false
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_managed_application_definition.percival.object_id

    secret_permissions = [
      "Get",
      "List",
      "Set"
    ]
  }
}
