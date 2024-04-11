terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.98.0"
    }
  }
}
resource "azurerm_resource_group" "global_resource_group" {
  name     = var.resource_group_name
  location = var.resource_group_location
}