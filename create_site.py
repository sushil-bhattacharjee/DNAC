import requests
import json
from rich import print
import urllib3
import time # Import time module for sleep functionality

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

####################### Code to Get the Token ###################
base_url = "https://10.10.20.85/api"
endpoint_url = "/system/v1/auth/token"

payload = ""
headers = {
    'content-type': 'application/json',
    'Authorization': 'Basic YWRtaW46Q2lzY28xMjM0IQ==',
    'Accept': 'application/json'
}

response = requests.request("POST", url=f"{base_url}{endpoint_url}", headers=headers, data=payload, verify=False)

try:
    response_json = response.json()
except requests.exceptions.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Raw Response Text: {response.text}")
    exit(1)

### Print the response and status code
print(f"HTTP Status Code: {response.status_code}")
Token = response_json.get('Token')
if not Token:
    print(f"[red]Token not found in response. Check API authentication.[/red]")
    exit(1)

print(f"[red]Token: {Token}")

####################### Get Network Devices ###################
req_headers = {
    'content-type': 'application/json',
    'Accept': 'application/json',
    'x-auth-token': Token
}

url = "https://10.10.20.85/dna/intent/api/v1"
endpoint = "/site"

payload = {
    "type": "area",
    "site": {
        "area": {
            "name": "WA",
            "parentName": "Global"
        }
    }
}

# payload_building = {
#     "type": "building",
#     "site": {
#         "building": {
#             "name": "HiTech",
#             "address": "string",
#             "parentName": "Sydney",
#             "latitude": "-33.847454",
#             "longitude": "151.073147",
#             "country": "Australia"
#         }
#     }
# }
response_site = requests.post(url=f"{url}{endpoint}", headers=req_headers, data=json.dumps(payload), verify=False)
print(f"HTTP response_site Status Code: {response_site.status_code}")
new_site_json = response_site.json()
print(json.dumps(new_site_json, indent=2))

# Wait for 50 seconds before running the next block of code
print("[yellow]Waiting for 50 seconds before fetching the site topology...[/yellow]")
time.sleep(50)

#############Print the newly created site##############

sites_endpoint = "/topology/site-topology"
sites_req = requests.get(url=f"{url}{sites_endpoint}", headers=req_headers, verify=False)
print(f"HTTP sites_req Status Code: {sites_req.status_code}")

sites_json = sites_req.json()
sites = sites_json['response']

# print(sites_req.text)
print(json.dumps(sites, indent=2))