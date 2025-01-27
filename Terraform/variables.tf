variable "subscription_id" {
  description = "The Azure SP subscription ID"
  type        = string
  sensitive   = true
}
variable "client_id" {
  description = "The Azure SP client ID"
  type        = string
  sensitive   = true
}
variable "client_secret" {
  description = "The Azure SP client secret"
  type        = string
  sensitive   = true
}
variable "tenant_id" {
  description = "The Azure SP tenant ID"
  type        = string
  sensitive   = true
}
variable "domeneshop_api_token" {
  description = "The Domeneshop API token"
  type        = string
  sensitive   = true
}
variable "domeneshop_api_secret" {
  description = "The Domeneshop API secret"
  type        = string
  sensitive   = true
}