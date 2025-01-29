# Domeneshop Azure Function App - API Documentation

This document provides details on the **Domeneshop Azure Function App API**, including available endpoints, authentication, and request/response formats.

---

## **🚀 Authentication**
All API requests require authentication using an **Azure Function Key**.

- **Header**: `x-functions-key`
- **Value**: Your **Azure Function Key** (stored securely)

---

## **📌 API Endpoints**
| **Method** | **Endpoint** | **Description** |
|-----------|-------------|----------------|
| **POST** | `/api/add_dns_txt` | Add a new DNS TXT record |
| **DELETE** | `/api/delete_dns_txt` | Remove an existing DNS TXT record |
| **GET** | `/api/list_domains` | Retrieve a list of domains |
| **GET** | `/api/list_txt_records?domain_name={domain}` | Retrieve TXT records for a given domain |

---

## **🔹 1. Add DNS TXT Record**
### **Request**
#### **Endpoint:**
```http
POST https://<YOUR_FUNCTION_APP>.azurewebsites.net/api/add_dns_txt
```

#### **Headers:**
```http
x-functions-key: <YOUR_FUNCTION_KEY>
Content-Type: application/json
```

#### **Body:**
```json
{
  "domain_id": "<DOMAIN_ID>",
  "record_name": "<RECORD_NAME>",
  "txt_value": "<TXT_VALUE>",
  "ttl": 3600  // Optional, default: 3600
}
```

### **Response**
#### ✅ **Success (201 Created)**
```json
{
  "message": "TXT record added successfully",
  "record_id": "<RECORD_ID>"
}
```

#### ❌ **Error (400 Bad Request)**
```json
{
  "error": "Missing required fields"
}
```

---

## **🔹 2. Delete DNS TXT Record**
### **Request**
#### **Endpoint:**
```http
DELETE https://<YOUR_FUNCTION_APP>.azurewebsites.net/api/delete_dns_txt
```

#### **Headers:**
```http
x-functions-key: <YOUR_FUNCTION_KEY>
Content-Type: application/json
```

#### **Body:**
```json
{
  "domain_id": "<DOMAIN_ID>",
  "record_id": "<RECORD_ID>"
}
```

### **Response**
#### ✅ **Success (200 OK)**
```json
{
  "message": "TXT record deleted successfully"
}
```

#### ❌ **Error (404 Not Found)**
```json
{
  "error": "Record not found"
}
```

---

## **🔹 3. List Domains**
### **Request**
#### **Endpoint:**
```http
GET https://<YOUR_FUNCTION_APP>.azurewebsites.net/api/list_domains
```

#### **Headers:**
```http
x-functions-key: <YOUR_FUNCTION_KEY>
```

### **Response**
#### ✅ **Success (200 OK)**
```json
{
  "domains": [
    {
      "domain_id": 123456,
      "domain_name": "example.com"
    },
    {
      "domain_id": 789012,
      "domain_name": "anotherdomain.com"
    }
  ]
}
```

---

## **🔹 4. List TXT Records**
### **Request**
#### **Endpoint:**
```http
GET https://<YOUR_FUNCTION_APP>.azurewebsites.net/api/list_txt_records?domain_name=<DOMAIN>
```

#### **Headers:**
```http
x-functions-key: <YOUR_FUNCTION_KEY>
```

### **Response**
#### ✅ **Success (200 OK)**
```json
{
  "records": [
    {
      "record_id": 654321,
      "record_name": "_acme-challenge",
      "txt_value": "challenge-token",
      "ttl": 3600
    },
    {
      "record_id": 987654,
      "record_name": "_other-record",
      "txt_value": "some-value",
      "ttl": 3600
    }
  ]
}
```

---

## **⚠️ Error Codes**
| **Status Code** | **Meaning** |
|---------------|------------|
| **200 OK** | Request was successful |
| **201 Created** | Resource was successfully created |
| **400 Bad Request** | Missing required parameters or invalid data |
| **401 Unauthorized** | Invalid API key |
| **403 Forbidden** | API key is missing or incorrect |
| **404 Not Found** | The requested resource does not exist |
| **500 Internal Server Error** | Unexpected server error |

---

## **📌 Deployment Instructions**
### **1️⃣ Setup Azure Function**
- Deploy the function using Terraform:
```bash
terraform init
terraform plan -out=tfplan
terraform apply -auto-approve tfplan
```

### **2️⃣ Store API Key Securely**
- Retrieve the **Azure Function Key** from the Azure portal.
- Store it securely and never expose it in repositories.

---

## **📄 License**
This project is licensed under the **MIT License**.

---

## **🔗 Related Resources**
- **Terraform Documentation**: [Terraform Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- **Domeneshop API**: [Domeneshop API Docs](https://api.domeneshop.no/docs)

