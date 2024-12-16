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

####################### Get Client Health ###################
req_headers = {
    'content-type': 'application/json',
    'Accept': 'application/json',
    'x-auth-token': Token
}

url = "https://10.10.20.85/dna/intent/api/v1"
endpoint = "/client-health"

response_clienthealth = requests.request("POST", url=f"{url}{endpoint}", headers=headers, verify=False)
print(f"HTTP response_Clienthealth Status Code: {response_clienthealth.status_code}")
response = response_clienthealth.json()
print(json.dumps(response, indent=2))

###############Printing client health scores#############
print(
    f"Clients: {response['response'][0]['scoreDetail'][0]['clientCount']}")


scores = response['response'][0]['scoreDetail']

for score in scores:
    if score['scoreCategory']['value'] == 'WIRED':
        print(f"Wired Clients: {score['clientCount']}")
        score_values = score['scoreList']
        for score_value in score_values:
            print(
                f"  {score_value['scoreCategory']['value']}: {score_value['clientCount']}")
    elif score['scoreCategory']['value'] == 'WIRELESS':
        print(f"Wireless Clients: {score['clientCount']}")
        score_values = score['scoreList']
        for score_value in score_values:
            print(
                f"  {score_value['scoreCategory']['value']}: {score_value['clientCount']}")