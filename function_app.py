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

def parse_and_validate_request(req: func.HttpRequest, required_params):
    """
    Parse and validate the HTTP request body for required parameters.
    """
    try:
        req_body = req.get_json()
    except ValueError:
        raise ValueError("Invalid JSON in request body.")

    missing_params = [param for param in required_params if not req_body.get(param)]
    if missing_params:
        raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

    return req_body

async def send_dns_request(domain_id, record_name, txt_value, ttl, api_token, api_secret):
    """
    Send an asynchronous HTTP POST request to add a DNS TXT record.
    """
    url = f"{DOMENESHOP_API_BASE_URL}/domains/{domain_id}/dns"
    data = {"type": "TXT", "host": record_name, "data": txt_value, "ttl": ttl}
    auth = (api_token, api_secret)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, auth=auth, headers=DOMENESHOP_API_HEADERS, json=data)

    if response.status_code == 201:
        return {
            "success": True,
            "message": "DNS TXT record added successfully.",
            "data": response.json(),
        }
    else:
        response_data = response.json() if response.content else {"error": "No response body"}
        return {
            "success": False,
            "message": f"Failed to add DNS TXT record. HTTP {response.status_code}",
            "error": response_data,
        }

@app.route(route="add_dns_txt", methods=["POST"])
async def add_dns_txt(req: func.HttpRequest) -> func.HttpResponse:
    """
    Handles HTTP POST requests to add a DNS TXT record.
    """
    logging.info("Processing a request to add a DNS TXT record.")

    try:
        # Retrieve environment variables
        api_token, api_secret = get_environment_variables()

        # Parse and validate the request body
        required_params = ["domain_id", "record_name", "txt_value"]
        req_body = parse_and_validate_request(req, required_params)

        # Extract parameters
        domain_id = req_body["domain_id"]
        record_name = req_body["record_name"]
        txt_value = req_body["txt_value"]
        ttl = req_body.get("ttl", DEFAULT_TTL)

        # Send the DNS request
        result = await send_dns_request(domain_id, record_name, txt_value, ttl, api_token, api_secret)

        # Return the result
        status_code = 200 if result["success"] else 400
        return func.HttpResponse(
            json.dumps(result), status_code=status_code, mimetype="application/json"
        )

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        return func.HttpResponse(str(ve), status_code=400)

    except httpx.RequestError as re:
        logging.error(f"HTTP request error: {re}")
        return func.HttpResponse(f"HTTP error: {str(re)}", status_code=500)

    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return func.HttpResponse("An unexpected error occurred.", status_code=500)

async def send_dns_delete_request(domain_id, record_id, api_token, api_secret):
    """
    Send an asynchronous HTTP DELETE request to remove a DNS TXT record.
    """
    url = f"{DOMENESHOP_API_BASE_URL}/domains/{domain_id}/dns/{record_id}"
    auth = (api_token, api_secret)

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, auth=auth, headers=DOMENESHOP_API_HEADERS)

    if response.status_code == 204:
        return {
            "success": True,
            "message": "DNS TXT record deleted successfully."
        }
    else:
        response_data = response.json() if response.content else {"error": "No response body"}
        return {
            "success": False,
            "message": f"Failed to delete DNS TXT record. HTTP {response.status_code}",
            "error": response_data,
        }

@app.route(route="delete_dns_txt", methods=["DELETE"])
async def delete_dns_txt(req: func.HttpRequest) -> func.HttpResponse:
    """
    Handles HTTP DELETE requests to remove a DNS TXT record.
    """
    logging.info("Processing a request to delete a DNS TXT record.")

    try:
        # Retrieve environment variables
        api_token, api_secret = get_environment_variables()

        # Parse and validate the request body
        required_params = ["domain_id", "record_id"]
        req_body = parse_and_validate_request(req, required_params)

        # Extract parameters
        domain_id = req_body["domain_id"]
        record_id = req_body["record_id"]

        # Send the DNS delete request
        result = await send_dns_delete_request(domain_id, record_id, api_token, api_secret)

        # Return the result
        status_code = 200 if result["success"] else 400
        return func.HttpResponse(
            json.dumps(result), status_code=status_code, mimetype="application/json"
        )

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        return func.HttpResponse(str(ve), status_code=400)

    except httpx.RequestError as re:
        logging.error(f"HTTP request error: {re}")
        return func.HttpResponse(f"HTTP error: {str(re)}", status_code=500)

    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return func.HttpResponse("An unexpected error occurred.", status_code=500)
