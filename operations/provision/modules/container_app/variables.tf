variable "resource_group_name" {
  description = "The name of the resource group"
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
variable "fastapi_container_app_name" {
  description = "The name of the container app"
  type        = string

}
variable "streamlit_container_app_name" {
  description = "The name of the container app"
  type        = string
  
}
variable "version_tag" {
  description = "The version tag of the container image"
  type        = string
  
}