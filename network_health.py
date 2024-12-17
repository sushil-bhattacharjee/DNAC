import requests
import json
from rich import print
import urllib3
from requests.exceptions import Timeout


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#######################Code to get the Token ###################
base_url = "https://10.10.20.85/api"
endpoint_url = "/system/v1/auth/token"


payload = ""
headers = {
  'content-type': 'application/json',
  'Authorization': 'Basic YWRtaW46Q2lzY28xMjM0IQ==',
  'Accept': 'application/json'
}

response = requests.request("POST", url=f"{base_url}{endpoint_url}", headers=headers, data=payload, verify=False)
response_json = response.json()

###Print the response and status code
# print(response.text)
print(f"HTTP Status Code: {response.status_code}")

###Print the response as json
# print(json.dumps(response_json, indent=2))
Token = response_json['Token']
print(f"[red]Token: {Token}")

######Network health ###############################
req_headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'x-auth-token': Token
}

dnac_url = "https://10.10.20.85"
NETWORK_HEALTH = '/dna/intent/api/v1/network-health'
response = requests.get(dnac_url + NETWORK_HEALTH, headers=req_headers, verify=False)
print("\n [blue]Printing the Netowrk-Health \n")
print(json.dumps(response.json(), indent=2))
network_health = response.json()['response']
print("\n [red]Network_health as filtered summary \n")
print('Good: {0}, Bad: {1}, Health score: {2}'.format(network_health[0]['goodCount'], network_health[0]['badCount'],network_health[0]['healthScore']))
