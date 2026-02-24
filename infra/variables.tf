variable "app_name" {
  description = "Application name"
  type        = string
  default     = "siemweb"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "francecentral"
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "siemweb-rg"
}