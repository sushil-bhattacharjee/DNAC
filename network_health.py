# trunk-ignore-all(black)
import requests
import json
from rich import print
import urllib3
from requests.exceptions import Timeout
import yaml

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#######################Code to get the Token ###################
# Base URL and Endpoint
base_url = "https://sandboxdnac2.cisco.com/dna/"
endpoint_url = "system/api/v1/auth/token"

# Headers
headers = {
    'content-type': 'application/json',
    'Authorization': "Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE="  # Replace with your valid token
}

# Make the Request
response = requests.post(f"{base_url}{endpoint_url}", headers=headers, verify=False)

# Print the Response Data Type
print(f"Response Data Type: {type(response.text)}")

# Debugging the Response
print(f"HTTP Status Code: {response.status_code}")
try:
    response_json = response.json()
    print(f"JSON Data Type for response_json(): {type(response_json)}")
    print(json.dumps(response_json, indent=2))
except requests.exceptions.JSONDecodeError:
    print("The response is not valid JSON.")
    print(f"Raw Response: {response.text}")
Token = response_json['Token']
print(f"[red]Token: {Token}")

######Network health ###############################
req_headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'x-auth-token': Token
}


NETWORK_HEALTH = 'intent/api/v1/network-health'
response = requests.get(base_url + NETWORK_HEALTH, headers=req_headers, verify=False, timeout=30)
print("\n [blue]Printing the Network-Health in HTTPs response str\n")
print(json.dumps(response.json(), indent=2))
# Print response in YAML format
print("\n[bold yellow]Response in YAML format:")
print(yaml.dump(response.json(), default_flow_style=False, sort_keys=False))

# Filter the response to get the network health summary 
#network_health = response.json()['response'] 
# #or the following
network_health = json.loads(response.text)

# Filter the response to get the healthDistribution for catergory Core
print("\n [bold yellow]HealthDistribution for catergory Core \n")
network_health = response.json()
for healthDist in network_health['healthDistirubution']:
    if healthDist['category'] == 'Core':
        print(json.dumps(healthDist, indent=2))
        print("\n [bold blue] Printing healthscore for Category=Core\n")
        print(healthDist['healthScore'])
        

