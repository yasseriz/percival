terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.98.0"
    }
  }
  backend "azurerm" {

  }
}

provider "azurerm" {
  features {

  }
}
module "resource_group" {
  source                  = "./modules/resource_group"
  resource_group_name     = var.resource_group_name
  resource_group_location = var.resource_group_location
}

module "storage" {
  source                   = "./modules/storage"
  depends_on               = [module.resource_group]
  resource_group_name      = var.resource_group_name
  storage_account_name     = var.storage_account_name
  storage_account_location = var.storage_account_location
  storage_account_type     = var.storage_account_type
}

module "key_vault" {
  source              = "./modules/key_vault"
  depends_on          = [module.resource_group]
  resource_group_name = var.resource_group_name
  key_vault_name      = var.key_vault_name
  key_vault_location  = var.key_vault_location
}

module "container_registry" {
  source                      = "./modules/container_registry"
  depends_on                  = [module.resource_group]
  resource_group_name         = var.resource_group_name
  container_registry_name     = var.container_registry_name
  container_registry_location = var.container_registry_location
}

module "container_app" {
  source                         = "./modules/container_app"
  depends_on                     = [module.resource_group, module.container_registry]
  resource_group_name            = var.resource_group_name
  container_app_environment_name = var.container_app_environment_name
  container_app_location         = var.container_app_location
}
