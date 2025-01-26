variable "subscription_id" {}
variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}
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