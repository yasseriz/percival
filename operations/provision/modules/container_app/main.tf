terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.98.0"
    }
  }
}

resource "azurerm_container_app_environment" "cenv" {
  name                       = var.container_app_environment_name
  location                   = var.container_app_location
  resource_group_name        = var.resource_group_name
}
resource "azurerm_container_app" "fastapi" {
  name                         = var.fastapi_container_app_name
  container_app_environment_id = azurerm_container_app_environment.cenv.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      name   = "fastapi-app"
      image  = "pptst01atmacrsea01.azurecr.io/percival/fastapi:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
}

resource "azurerm_container_app" "streamlit" {
  name                         = var.streamlit_container_app_name
  container_app_environment_id = azurerm_container_app_environment.cenv.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      name   = "fastapi-app"
      image  = "pptst01atmacrsea01.azurecr.io/percival/streamlit:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
}