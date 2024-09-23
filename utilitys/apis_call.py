import requests

def call_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        print(f"API called: {url}, Status code: {response.status_code}")
        statuscode =response.status_code
        # Check if the request was successful (status code 200-299)
        if response.status_code >= 200 and response.status_code < 300:
            return {'status': True, "status_code": str(response.status_code), "data": ""}
        else:
            return {'status': False, "status_code": str(response.status_code), "data": ""}
    except requests.exceptions.HTTPError as http_err:
        # This block will capture HTTP-related errors (4xx, 5xx)
        print(f"HTTP error occurred: {http_err}")
        return {'status': False, "status_code": str(http_err.response.status_code), "data": str(http_err)}
    except requests.exceptions.RequestException as e:
        # This block will capture other exceptions (network errors, timeouts, etc.)
        print(f"Error calling API: {e}")
        return {'status': False, "status_code": 404, "data": str(e)}


import requests
import json


def post_api(url, data):
    try:
        # Set headers for JSON data
        headers = {'Content-Type': 'application/json'}

        # Send POST request
        response = requests.post(url, headers=headers, json=data)

        # Check if the request was successful (status code 200-299)
        if response.status_code >= 200 and response.status_code < 300:
            print("Request was successful:", response.json())
            return {'status': True, "status_code": str(response.status_code), "data": []}
        else:
            print(f"Failed with status code {response.status_code}: {response.text}")
            return {'status': False, "status_code": str(response.status_code), "data": []}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {'status': False, "status_code": str(response.status_code), "data": str(e)}


# # Example usage
# url = 'https://notifyservisesrc.azurewebsites.net/notify/sendmail'  # Replace with your API URL
# data = {
#     "superid": 41112,
#     "toaddr": "pavan@perennialcode.in",
#     "message": "test tamplate 11",
#     "subject": "test mail working  or not"
# }
#
# post_api(url, data)
