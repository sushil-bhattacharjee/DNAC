import requests
import json
from rich import print
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
print(response.text)
print(f"HTTP Status Code: {response.status_code}")

###Print the response as json
print(json.dumps(response_json, indent=2))
Token = response_json['Token']
print(Token)

req_headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'x-auth-token': Token
}