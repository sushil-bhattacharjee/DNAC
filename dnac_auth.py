import requests
import json
from rich import print
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# base_url = "https://10.10.20.85/api"
base_url = "https://sandboxdnac2.cisco.com/dna"
endpoint_url = "/system/api/v1/auth/token"


payload = ""
headers = {
  'content-type': 'application/json',
  'Authorization': 'Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE=',
  'Accept': 'application/json'
}

response = requests.request("POST", url=f"{base_url}{endpoint_url}", headers=headers, data=payload, verify=False)


#Print the response and status code
print(f"Raw Response Text: {response.text}")
print(f"HTTP Status Code: {response.status_code}")

response_json = response.json()

###Print the response and status code


###Print the response as json
print(json.dumps(response_json, indent=2))
Token = response_json['Token']
print(Token)

req_headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'x-auth-token': Token
}