variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string

}

variable "resource_group_location" {
  description = "The location of the resource group"
  type        = string

}
variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
}
variable "storage_account_location" {
  description = "The location of the storage account"
  type        = string

}
variable "storage_account_type" {
  description = "The type of replication to use for this storage account"
  type        = string

}
variable "key_vault_name" {
  description = "The name of the key vault"
  type        = string
}

variable "key_vault_location" {
  description = "The location of the key vault"
  type        = string

}
variable "container_registry_name" {
  description = "The name of the container registry"
  type        = string

}
variable "container_registry_location" {
  description = "The location of the container registry"
  type        = string

}
variable "container_app_environment_name" {
  description = "The name of the container app environment"
  type        = string

}
variable "container_app_location" {
  description = "The location of the container app"
  type        = string

}
