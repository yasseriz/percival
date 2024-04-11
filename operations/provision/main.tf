terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
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
  source = "./modules/resource_group"
  resource_group_name = var.resource_group_name
  resource_group_location = var.resource_group_location
}

module "storage"{ 
  source = "./modules/storage"
  depends_on = [ module.resource_group ]
  resource_group_name = var.resource_group_name
  storage_account_name = var.storage_account_name
  storage_account_location = var.storage_account_location
  storage_account_type = var.storage_account_type
}
