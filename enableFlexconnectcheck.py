"""Module for checking FlexConnect status in Cisco DNA Center wireless profiles."""
import os
import sys
import requests
import urllib3
from rich import print as console_print

urllib3.disable_warnings()

def get_dnac_wireless_profiles(token):
    """Get DNAC wireless profiles"""
    try:
        url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/wireless/profile"
        headers = {"X-Auth-Token": token}
        response = requests.get(url, headers=headers, verify=False, timeout=30)  # nosec
        # return response.json()
        return response.json()[0]['profileDetails']['ssidDetails'][0]['flexConnect']['enableFlexConnect']
    except Exception as e:
        console_print(e)
        sys.exit(1)

def create_dnac_token():
    """Create DNAC token"""
    try:
        url = "https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {os.getenv('DNAC_USERNAME')}:{os.getenv('DNAC_PASSWORD')}"
        }
        response = requests.post(url, headers=headers, verify=False, timeout=30)  # nosec
        return response.json()["Token"]
    except Exception as e:
        console_print(e)
        sys.exit(1)

if __name__ == "__main__":
    token = create_dnac_token()
    console_print(get_dnac_wireless_profiles(token))


    """ Original response.json()
    [
    {
        'profileDetails': {
            'instanceUuid': '1d9b96fe-6ffe-455b-8226-2fc6a9b12c67',
            'name': 'Enter',
            'ssidDetails': [{'name': 'Enterprise', 'enableFabric': True, 'flexConnect': {'enableFlexConnect': False}, 'interfaceName': ''}],
            'sites': []
        }
    },
    {'profileDetails': {'instanceUuid': '4529134d-fb6c-445e-a288-1412d36f94c4', 'name': 'gh', 'ssidDetails': [], 'sites': []}},
    {'profileDetails': {'instanceUuid': '211510a5-bf3e-4700-ba6e-5345f7dc53df', 'name': 'Student1_Wireless', 'ssidDetails': [], 'sites': []}}
]
    """