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

######Get sites ###############################
req_headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'x-auth-token': Token
}


dnac_url = "https://10.10.20.85:443"

sess = requests.session()
try:
    rc = sess.request('GET', dnac_url, headers=req_headers, timeout=1, verify=False)
except Timeout:
    print('TIMEOUT ERROR: Unable to access DNA Center!')
    exit(-1)

if rc.status_code == requests.codes.ok:  # Correct Option
    print('The request was successful!')
else:
    print(f'Error Code: {rc.status_code} : {rc.reason}')  # Correct Options