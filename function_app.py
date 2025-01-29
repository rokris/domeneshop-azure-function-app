import azure.functions as func
import logging
import os
import json
import httpx

# Constants
DOMENESHOP_API_BASE_URL = "https://api.domeneshop.no/v0"
DOMENESHOP_API_HEADERS = {"Content-Type": "application/json"}
DEFAULT_TTL = 3600  # Default TTL for DNS records

# Initialize the function app for Programming Model V2
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_environment_variables():
    """
    Retrieve and validate required environment variables.
    """
    api_token = os.getenv("DOMENESHOP_API_TOKEN")
    api_secret = os.getenv("DOMENESHOP_API_SECRET")
    if not api_token or not api_secret:
        raise ValueError("Missing required API credentials: DOMENESHOP_API_TOKEN and DOMENESHOP_API_SECRET")
    return api_token, api_secret

async def send_api_request(endpoint, api_token, api_secret, method="GET", data=None):
    """
    Send an asynchronous HTTP request to the Domeneshop API.
    """
    url = f"{DOMENESHOP_API_BASE_URL}{endpoint}"
    auth = (api_token, api_secret)

    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url, auth=auth, headers=DOMENESHOP_API_HEADERS)
        elif method == "POST":
            response = await client.post(url, auth=auth, headers=DOMENESHOP_API_HEADERS, json=data)
        elif method == "DELETE":
            response = await client.delete(url, auth=auth, headers=DOMENESHOP_API_HEADERS)
        else:
            raise ValueError("Unsupported HTTP method")

    return response

@app.route(route="list_domains", methods=["GET"])
async def list_domains(req: func.HttpRequest) -> func.HttpResponse:
    """
    Lists all domains and their corresponding domain_id.
    """
    logging.info("Processing a request to list all domains.")
    try:
        api_token, api_secret = get_environment_variables()
        response = await send_api_request("/domains", api_token, api_secret)

        if response.status_code == 200:
            return func.HttpResponse(response.text, status_code=200, mimetype="application/json")
        else:
            return func.HttpResponse(f"Failed to retrieve domains. HTTP {response.status_code}", status_code=400)

    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return func.HttpResponse("An unexpected error occurred.", status_code=500)

@app.route(route="list_txt_records", methods=["GET"])
async def list_txt_records(req: func.HttpRequest) -> func.HttpResponse:
    """
    Lists all TXT records for a specified domain_name.
    """
    logging.info("Processing a request to list TXT records for a domain.")
    try:
        api_token, api_secret = get_environment_variables()
        domain_name = req.params.get("domain_name")
        
        if not domain_name:
            return func.HttpResponse("Missing required parameter: domain_name", status_code=400)
        
        response = await send_api_request("/domains", api_token, api_secret)
        if response.status_code != 200:
            return func.HttpResponse(f"Failed to retrieve domains. HTTP {response.status_code}", status_code=400)
        
        domains = response.json()
        domain = next((d for d in domains if d["domain"] == domain_name), None)
        
        if not domain:
            return func.HttpResponse(f"Domain {domain_name} not found.", status_code=404)
        
        domain_id = domain["id"]
        records_response = await send_api_request(f"/domains/{domain_id}/dns", api_token, api_secret)
        
        if records_response.status_code == 200:
            txt_records = [record for record in records_response.json() if record["type"] == "TXT"]
            return func.HttpResponse(json.dumps(txt_records), status_code=200, mimetype="application/json")
        else:
            return func.HttpResponse(f"Failed to retrieve TXT records. HTTP {records_response.status_code}", status_code=400)

    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return func.HttpResponse("An unexpected error occurred.", status_code=500)

@app.route(route="add_dns_txt", methods=["POST"])
async def add_dns_txt(req: func.HttpRequest) -> func.HttpResponse:
    """
    Handles HTTP POST requests to add a DNS TXT record.
    """
    logging.info("Processing a request to add a DNS TXT record.")
    try:
        api_token, api_secret = get_environment_variables()
        req_body = req.get_json()
        domain_id = req_body["domain_id"]
        record_name = req_body["record_name"]
        txt_value = req_body["txt_value"]
        ttl = req_body.get("ttl", DEFAULT_TTL)
        data = {"type": "TXT", "host": record_name, "data": txt_value, "ttl": ttl}
        result = await send_api_request(f"/domains/{domain_id}/dns", api_token, api_secret, method="POST", data=data)
        return func.HttpResponse(json.dumps(result.json()), status_code=result.status_code, mimetype="application/json")
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return func.HttpResponse("An unexpected error occurred.", status_code=500)

@app.route(route="delete_dns_txt", methods=["DELETE"])
async def delete_dns_txt(req: func.HttpRequest) -> func.HttpResponse:
    """
    Handles HTTP DELETE requests to remove a DNS TXT record.
    """
    logging.info("Processing a request to delete a DNS TXT record.")
    try:
        api_token, api_secret = get_environment_variables()
        req_body = req.get_json()
        domain_id = req_body["domain_id"]
        record_id = req_body["record_id"]
        result = await send_api_request(f"/domains/{domain_id}/dns/{record_id}", api_token, api_secret, method="DELETE")
        return func.HttpResponse(json.dumps(result.json()), status_code=result.status_code, mimetype="application/json")
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return func.HttpResponse("An unexpected error occurred.", status_code=500)
