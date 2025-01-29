# Azure Function App for Managing DNS TXT Records with Domeneshop
[![Super-Linter](https://github.com/rokris/domeneshop-azure-function-app/actions/workflows/superlint.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)

This Azure Function enables the addition of DNS TXT records to the Domeneshop DNS service via HTTP requests.
---

[Link to API-documentation](./API_DOCUMENTATION.md)
---

## **Prerequisites**

- Fork or clone the GitHub repository.
- Create **DOMENESHOP_API_TOKEN** and **DOMENESHOP_API_SECRET** on the Domeneshop website.
  - Store the token and secret in **GitHub Actions secrets** and variables.
- Create an **Azure Service Principal**.
  - Store the JSON in GitHub secrets under `AZURE_SP_JSON`.

```bash
az ad sp create-for-rbac --name <name> --role Contributor --scopes /subscriptions/<Subscription-ID> --json-auth

az role assignment create \
  --assignee <Application ID> \
  --role "User Access Administrator" \
  --scope /subscriptions/<Subscription-ID>
```

- Create **GitHub Personal Access Tokens (Classic)** with the required permissions (`repo`, `workflow`, `admin:repo_hook`).
  - Store the token in **GitHub Secrets** under `TERRAFORM_GITHUB_TOKEN`.
- Run the workflow **"Terraform Azure Deployment"** to create the Azure resources (**Run this workflow only once**).
  - If the parameter is set to `false`, execution will stop after the planning step.
- Run the GitHub workflow to:
  - **Build and deploy** the Python project to **Azure Function App** - `<YOUR_FUNCTION_APP_NAME>`.

---

## **Usage Example with HTTPie**

You can interact with the Azure Function using **HTTPie**. Below are examples of how to make requests:

### **Add a DNS TXT Record**
```bash
http POST https://<YOUR_FUNCTION_APP_NAME>.azurewebsites.net/api/add_dns_txt \
    x-functions-key:<YOUR_FUNCTION_KEY> \
    Content-Type:application/json \
    domain_id=<YOUR_DOMAIN_ID> \
    record_name="<YOUR_RECORD_NAME>" \
    txt_value="<YOUR_TXT_VALUE>" \
    ttl:=3600  # Optional
```

### **Delete a DNS TXT Record**
```bash
http DELETE https://<YOUR_FUNCTION_APP_NAME>.azurewebsites.net/api/delete_dns_txt \
    x-functions-key:<YOUR_FUNCTION_KEY> \
    Content-Type:application/json \
    domain_id=<YOUR_DOMAIN_ID> \
    record_id=<YOUR_RECORD_ID>
```

### **List Domains**
```bash
http GET https://<YOUR_FUNCTION_APP_NAME>.azurewebsites.net/api/list_domains \
    x-functions-key:<YOUR_FUNCTION_KEY>
```

### **List TXT Records for a Domain**
```bash
http GET "https://<YOUR_FUNCTION_APP_NAME>.azurewebsites.net/api/list_txt_records?domain_name=example.com" \
    x-functions-key:<YOUR_FUNCTION_KEY>
```

### **Replace the Following Placeholders:**
- `<YOUR_FUNCTION_APP_NAME>`: Your **Azure Function App** name.
- `<YOUR_FUNCTION_KEY>`: The **Function Key** for authentication.
- `<YOUR_DOMAIN_ID>`, `<YOUR_RECORD_ID>`, `<YOUR_RECORD_NAME>`, and `<YOUR_TXT_VALUE>` with your **actual values**.

---

## **Running Locally on Your Desktop**

To test this function locally, create the following file in the root of your project:

### **`local.settings.json`**
This file stores environment variables for local development.

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DOMENESHOP_API_TOKEN": "your_api_token",
    "DOMENESHOP_API_SECRET": "your_api_secret",
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
- Ensure that **Domeneshop API Token** and **API Secret** are securely stored and **not exposed in version control**.
- If running locally, ensure your environment is set up with Python and the required dependencies:

```bash
pip install -r requirements.txt
```
