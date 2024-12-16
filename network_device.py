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
response_json = response.json()

### Print the response and status code
print(f"HTTP Status Code: {response.status_code}")
Token = response_json['Token']
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

ntk_dev_json = ntk_dev_req.json()
network_devices = ntk_dev_json['response']

print("[blue]Network Devices List \n")
print(json.dumps(network_devices, indent=2))

####################### Print VLANs for Each Hostname ###################
for device in network_devices:
    hostname = device.get('hostname', 'Unknown')
    dev_id = device.get('id', None)

    if dev_id:  # Only fetch VLANs if the device ID exists
        print(f"[green]Fetching VLANs for Hostname: {hostname}[/green]")
        dev_vlan_endpoint = f"/intent/api/v1/network-device/{dev_id}/vlan"
        vlan_req = requests.get(url=f"{url}{dev_vlan_endpoint}", headers=req_headers, verify=False)

        if vlan_req.status_code == 200:
            dev_vlans = vlan_req.json().get('response', [])
            print(f"[yellow]VLANs for {hostname}: [/yellow]")
            print(json.dumps(dev_vlans, indent=2))
        else:
            print(f"[red]Failed to fetch VLANs for {hostname}. HTTP Status: {vlan_req.status_code}[/red]")
    else:
        print(f"[red]Device ID not found for Hostname: {hostname}[/red]")
