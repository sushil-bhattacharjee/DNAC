"""Module for retrieving wireless health statistics from Cisco DNA Center sites."""
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
if response.status_code == 200:
    site_response = response.json()['response']
    for site in site_response:
        console_print(f"{site['siteName']}: {site['networkHealthWireless']}")
else:
    console_print(response.status_code, response.text)
