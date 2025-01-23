import requests
import urllib3
from rich import print as console_print

urllib3.disable_warnings()

def get_dnac_wireless_profiles(token):
    """Get DNAC wireless profiles"""
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/wireless/profile"
    headers = {"X-Auth-Token": token}
    response = requests.get(url, headers=headers, verify=False, timeout=30)  # nosec
    # return response.json()
    return response.json()[0]['profileDetails']['ssidDetails'][0]['flexConnect']['enableFlexConnect']

def create_dnac_token():
    """Create DNAC token"""
    url = "https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE="
    }
    response = requests.post(url, headers=headers, verify=False, timeout=30)  # nosec
    return response.json()["Token"]

if __name__ == "__main__":
    token = create_dnac_token()
    console_print(get_dnac_wireless_profiles(token))
