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
print(f"HTTP response Status Code: {response.status_code}")
Token = response_json.get('Token')
if not Token:
    print(f"[red]Token not found in response. Check API authentication.[/red]")
    exit(1)

print(f"[red]Token: {Token}")

####################### Get Credentials from the DNAC for CLI and SNMPV2 ###################
req_headers = {
    'content-type': 'application/json',
    'Accept': 'application/json',
    'x-auth-token': Token
}

url = "https://10.10.20.85/dna/intent/api/v1"
cli_endpoint = "/global-credential?credentialSubType=CLI"
snmp_endpoint = "/global-credential?credentialSubType=SNMPV2_WRITE_COMMUNITY"

cli_credentials = requests.get(url=f"{url}{cli_endpoint}", headers=req_headers, verify=False).json()
snmp_credentials = requests.get(url=f"{url}{snmp_endpoint}", headers=req_headers, verify=False).json()

print("\n [red] CLI Credential \n")
print(json.dumps(cli_credentials, indent=2))
print("\n [blue] SNMPV2_WRITE community")
print(json.dumps(snmp_credentials, indent=2))


cli_cred_id = cli_credentials['response'][0]["id"]
snmp_cred_id = snmp_credentials['response'][0]["id"]

print(f"\n[blue] cli_cred_id = {cli_cred_id}\n")
print(f"\n[red] snmp_cred_id = {snmp_cred_id}\n")

payload_discovery = {
    "name": "CML2.8 BOND lab's Discovery in Sandbox Catalyst Centre",
    "discoveryType": "Range",
    "ipAddressList": "10.1.10.10-10.1.10.21",
    "timeout": 1,
    "protocolOrder": "ssh,telnet",
    "preferredMgmtIPMethod": "None",
    "globalCredentialIdList": [cli_cred_id, snmp_cred_id]
}

discovery_endpoint = "/discovery"
discv_response = requests.post(url=f"{url}{discovery_endpoint}", headers=req_headers, data=json.dumps(payload_discovery), verify=False)
print(f"HTTP response code for disc_response: {discv_response.status_code}")
discovery = discv_response.json()
print(json.dumps(discovery, indent=2))