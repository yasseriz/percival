terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.98.0"
    }
  }
}

resource "azurerm_container_app_environment" "cenv" {
  name                = var.container_app_environment_name
  location            = var.container_app_location
  resource_group_name = var.resource_group_name
}