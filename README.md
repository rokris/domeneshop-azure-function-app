# Azure Function App for Managing DNS TXT Records with Domeneshop

This Azure Function enables the addition of DNS TXT records to the Domeneshop DNS service via HTTP requests.

---

## **Prereq**

- Clone the GitHub repo
- Create DOMENESHOP_API_TOKEN and DOMENESHOP_API_SECRET at Domeneshop website
- Create a Service Principal
- Run the Terraform to create the Azure Function App (use SP values)
- Create a Managed Identity in Azure
- Store Federated credentials in GitHub secrets
- Configure the Deployment Center in Azure Funtion App using Managed Identity

```bash
az ad sp create-for-rbac --name "github-terraform-deploy" --role Contributor --scopes /subscriptions/<subscription-id> --json-auth
```

```bash
az role assignment create \
  --assignee cbb206df-ab25-4f45-9c6c-02a0f1da103e \
  --role "User Access Administrator" \
  --scope /subscriptions/edbad54f-b52a-4f78-9016-0ac27a6fee55
```

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
- If running locally, ensure your environment is set up with Python and the required dependencies (`azure-functions`, `requests`, etc.).

---
