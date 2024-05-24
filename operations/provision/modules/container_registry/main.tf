terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.98.0"
    }
  }
}

data "azurerm_managed_application_definition" "percival" {
  name                = var.managed_app_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_container_registry" "acr" {
  name                = var.container_registry_name
  resource_group_name = var.resource_group_name
  location            = var.container_registry_location
  sku                 = "Standard"
  admin_enabled       = false
  identity {
    type         = "UserAssigned"
    identity_ids = ["${data.azurerm_managed_application_definition.percival.object_id}"]
  }
}
