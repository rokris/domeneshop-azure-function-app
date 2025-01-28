# Azure Function App for Managing DNS TXT Records with Domeneshop

This Azure Function enables the addition of DNS TXT records to the Domeneshop DNS service via HTTP requests.

---

## **Prereq**

- Fork or Clone the GitHub repository to your own repository
- Create DOMENESHOP_API_TOKEN and DOMENESHOP_API_SECRET at Domeneshop website
  * Store token and secret in Github Actions secrets and variables
- Create a Azure Service Principal
  * Store the JSON in Github secrets under AZURE_SP_JSON

```bash
az ad sp create-for-rbac --name <name> --role Contributor --scopes /subscriptions/<Subscription-ID> --json-auth

az role assignment create \
  --assignee <Application ID> \
  --role "User Access Administrator" \
  --scope /subscriptions/<Subscription ID>
```

- Create GitHub Personal access tokens (classic) ( repo, workflow, admin:repo_hook ? )
  * Store tokens in Github Secrets under name TERRAFORM_GITHUB_TOKEN 
- Run the workflow "Terraform Azure Deployment" to create the Azure resources (Run the workflow only once).
  * Parameter = false, will abort running after the planning step.
- Run GitHub workflow
  * Build and deploy Python project to Azure Function App - domeneshop-azure-function-app

---

## **Usage Example with HTTPie**

You can interact with the Azure Function using **HTTPie**. Below is an example of how to make a request to add a DNS TXT record:

```bash
http POST https://<FUNCTION_APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME> \
    x-functions-key:xxxxxxxxxxxxxxxxxxxxxxxxx \
    Content-Type:application/json \
    domain_id= \
    record_name="" \
    txt_value="" \
    ttl:=3600 --> optional
```

```bash
http DELETE https://<FUNCTION_APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME> \
     x-functions-key:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
     Content-Type:application/json \
     domain_id= \
     record_id=
```

Replace the following:

- `<FUNCTION_APP_NAME>`: The name of your Azure Function App.
- `<FUNCTION_NAME>`: The name of your Azure Function.
- `xxxxxxxxxxxxxxxxxxxxxxxxx`: The Function Key for authentication.
- Update `domain_id`, `record_id`, record_name`, and `txt_value` with your actual values.

---

## **Running Locally on Your Desktop**

To test this function locally, create the following file in the root of your project:

### `local.settings.json`

This file is used to store environment variables for local development. Below is an example:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DOMENESHOP_API_TOKEN": "xxxxxxxxxxxxxxxx",
    "DOMENESHOP_API_SECRET": "xxxxxxxxxxxxxxxxxxxxxxx",
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE": false
  },
  "Host": {
    "LocalHttpPort": 7071,
    "CORS": "*",
    "CORSCredentials": false
  }
}
```
---

## **Notes**

- Ensure the **Domeneshop API Token** and **API Secret** are securely stored and not exposed in version control.
- If running locally, ensure your environment is set up with Python and the required dependencies (`azure-functions`, `httpx`, etc.).

```bash
pip install -r requirements.txt
```
---
