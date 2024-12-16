import requests
import json
from rich import print
import urllib3


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
print(f"Token: {Token}")

######Get sites ###############################
req_headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'x-auth-token': Token
}
url = "https://10.10.20.85/dna"
sites_endpoint = "/intent/api/v1/topology/site-topology"
# trunk-ignore(bandit/B113)
sites_req = requests.get(url=f"{url}{sites_endpoint}", headers=req_headers, verify=False)
print(f"HTTP sites_req Status Code: {sites_req.status_code}")

sites_json = sites_req.json()
sites = sites_json['response']

# print(sites_req.text)
print(json.dumps(sites, indent=2))


