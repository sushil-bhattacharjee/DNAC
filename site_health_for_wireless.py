import json
import os
import requests
import urllib3
from rich import print as console_print

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get the token
token = os.getenv('DNAC_AUTH_TOKEN')

# Get the site health
SITE_HEALTH_URL = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/site-health"
headers = {'X-Auth-Token': token}
response = requests.get(SITE_HEALTH_URL, headers=headers, verify=False, timeout=30)  # nosec
console_print(response.json())
