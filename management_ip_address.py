import requests
import json
from rich import print
import urllib3

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

url = "https://10.10.20.85/dna"
endpoint = "/intent/api/v1/network-device"

ntk_dev_req = requests.get(url=f"{url}{endpoint}", headers=req_headers, verify=False)
print(f"HTTP ntk_dev_req Status Code: {ntk_dev_req.status_code}")

try:
    ntk_dev_json = ntk_dev_req.json()
except requests.exceptions.JSONDecodeError as e:
    print(f"Failed to parse network devices JSON: {e}")
    print(f"Raw Response Text: {ntk_dev_req.text}")
    exit(1)

network_devices = ntk_dev_json.get('response', [])

####################### Print Management IP Address for Each Device ###################
print("[blue]Device Management IP Addresses:[/blue]\n")
for device in network_devices:
    hostname = device.get('hostname', 'Unknown')
    management_ip = device.get('managementIpAddress', 'Not Available')

    if management_ip == 'Not Available':
        print(f"[red]Skipping device with hostname {hostname} as it has no management IP[/red]")
        continue

    print(f"[green]Hostname:[/green] {hostname}, [yellow]Management IP Address:[/yellow] {management_ip}")

    #### Print SDA Information for Each Device ####
    sda_endpoint = f"/intent/api/v1/business/sda/device?deviceIPAddress={management_ip}"
    sda_req = requests.get(url=f"{url}{sda_endpoint}", headers=req_headers, verify=False)
    print(f"HTTP sda response Status Code: {sda_req.status_code}")

    try:
        response_sda = sda_req.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Failed to parse SDA JSON for {hostname}: {e}")
        print(f"Raw Response Text: {sda_req.text}")
        continue

    print(f"[yellow]SDA Information for {hostname}:[/yellow]")
    print(json.dumps(response_sda, indent=2))

