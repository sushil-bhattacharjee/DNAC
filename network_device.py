"""Module for retrieving network device information and VLANs from Cisco DNA Center."""
import json
import os
import base64
import sys
import requests
from dotenv import load_dotenv
from rich import print as console_print
import urllib3

# Load environment variables from .env file
load_dotenv()
# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://sandboxdnac2.cisco.com/"

auth_token = os.getenv('DNAC_AUTH_TOKEN')

####################### Get Network Devices ###################
def get_dnac_devices(auth_token, base_url):
    """Get network devices from DNA Center."""
    try:
        req_headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
            'x-auth-token': auth_token
        }
        endpoint_url = "dna/intent/api/v1/network-device"

        ntk_dev_req = requests.get(url=f"{base_url}{endpoint_url}", headers=req_headers, verify=False, timeout=30)  # nosec
        ntk_dev_req.raise_for_status()
        network_devices = ntk_dev_req.json()['response']
        console_print("[blue]Network Devices List \n")
        console_print(json.dumps(network_devices, indent=2))
        return network_devices
    except Exception as e:
        if str(requests.status_code.codesUNAUTHORIZED) in str(e):
            create_dnac_token()

def get_device_vlans(token, network_devices, base_url):
    """Get VLANs for each network device."""
    req_headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'x-auth-token': token
    }
    
    for device in network_devices:
        hostname = device.get('hostname', 'Unknown')
        if dev_id := device.get('id'):
            console_print(f"[green]Fetching VLANs for Hostname: {hostname}[/green]")
            dev_vlan_endpoint = f"dna/intent/api/v1/network-device/{dev_id}/vlan"
            vlan_req = requests.get(url=f"{base_url}{dev_vlan_endpoint}", headers=req_headers, verify=False, timeout=30)  # nosec

            if vlan_req.status_code == 200:
                dev_vlans = vlan_req.json().get('response', [])
                console_print(f"[yellow]VLANs for {hostname}: [/yellow]")
                console_print(json.dumps(dev_vlans, indent=2))
            else:
                console_print(f"[red]Failed to fetch VLANs for {hostname}. HTTP Status: {vlan_req.status_code}[/red]")
        else:
            console_print(f"[red]Device ID not found for Hostname: {hostname}[/red]")
            
####################### Code to Get the Token ###################
def create_dnac_token():
    """Create authentication token for DNA Center API access."""
    try:
        endpoint_url = "/api/system/v1/auth/token"
        credentials = f"{os.getenv('DNAC_USERNAME')}:{os.getenv('DNAC_PASSWORD')}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            'content-type': 'application/json',
            'Authorization': f"Basic {encoded_credentials}", 
            'Accept': 'application/json'
        }
        response = requests.post(
            url=f"{BASE_URL}{endpoint_url}", 
            headers=headers, 
            verify=False, 
            timeout=30
        )  # nosec
        response.raise_for_status()
        Token = response.json()['Token']
        console_print(f"[red]Token: {Token}")
        return Token
    except Exception as e:
        if str(response.status_code.codes.SERVER_ERROR) in str(e):
            sys.exit("DNAC Service is not available")

if __name__ == "__main__":
    token = create_dnac_token()
    devices = get_dnac_devices(token, BASE_URL)
    get_device_vlans(token, devices, BASE_URL)
