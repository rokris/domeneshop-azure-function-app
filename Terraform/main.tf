terraform {
  required_version = ">=1.2"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.50.0"
    }

    github = {
      source  = "integrations/github"
      version = ">= 4.0.0"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

provider "github" {
  token = var.github_token
  owner = var.github_organization_name
}

resource "azurerm_resource_group" "rg" {
  name     = "ng-ti-test-rokris-domeneshop-azure-rg"
  location = "Norway East"
}

resource "azurerm_user_assigned_identity" "base" {
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  name                = "ng-ti-rokris-github-azure-mi"
}

resource "azurerm_role_assignment" "role" {
  principal_id         = azurerm_user_assigned_identity.base.principal_id
  role_definition_name = "Website Contributor"
  scope                = azurerm_resource_group.rg.id
}

resource "azurerm_federated_identity_credential" "fc" {
  name                = "rokris-domeneshop-azure-function-app"
  parent_id           = azurerm_user_assigned_identity.base.id
  resource_group_name = azurerm_resource_group.rg.name
  audience            = ["api://AzureADTokenExchange"] # Common audience for OIDC
  issuer              = "https://token.actions.githubusercontent.com" # Replace with your identity provider's issuer
  subject             = "repo:rokris/domeneshop-azure-function-app:ref:refs/heads/master" # Replace with your specific repo and branch
}

data "github_repository" "this" {
  name = var.github_repository_name
}

resource "github_actions_secret" "azure_client_id" {
  repository      = data.github_repository.this.name
  secret_name     = "AZUREAPPSERVICE_CLIENTID"
  plaintext_value = azurerm_user_assigned_identity.base.client_id
}

resource "github_actions_secret" "azure_tenant_id" {
  repository      = data.github_repository.this.name
  secret_name     = "AZUREAPPSERVICE_TENANTID"
  plaintext_value = azurerm_user_assigned_identity.base.tenant_id
}

resource "github_actions_secret" "azure_subscription_id" {
  repository      = data.github_repository.this.name
  secret_name     = "AZUREAPPSERVICE_SUBSCRIPTIONID"
  plaintext_value = var.subscription_id
}

resource "azurerm_storage_account" "sa" {
  name                     = "domeneshopazure"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "asp" {
  name                = "domeneshop-azure-function-app-sp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku_name            = "Y1" # Dynamic Consumption Plan
  os_type             = "Linux"
}

resource "azurerm_linux_function_app" "func" {
  name                       = "domeneshop-azure-function-app"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  service_plan_id            = azurerm_service_plan.asp.id  # Link to the Service Plan
  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key

  site_config {
    ftps_state                  = "Disabled"
    application_stack {
      python_version              = "3.10"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME            = "python"
    AzureWebJobsStorage                 = azurerm_storage_account.sa.primary_connection_string
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false" # Add environment variable
    DOMENESHOP_API_TOKEN                = var.domeneshop_api_token
    DOMENESHOP_API_SECRET               = var.domeneshop_api_secret
  }

  identity {
    type = "SystemAssigned"
  }
}