"""Module for retrieving wireless health statistics from Cisco DNA Center sites."""
import json
import os
from dotenv import load_dotenv
import requests
import urllib3
from rich import print as console_print

# Load environment variables from .env file
load_dotenv()

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get the token
token = os.getenv('DNAC_AUTH_TOKEN')

# Get the site health
SITE_HEALTH_URL = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/site-health"
headers = {'X-Auth-Token': token}
response = requests.get(SITE_HEALTH_URL, headers=headers, verify=False, timeout=30)  # nosec
# Get initial response data
response_data = response.json()

# Extract response list
sites = response_data['response']

# Calculate total pages
page_size = 3
total_pages = (len(sites) + page_size - 1) // page_size

# Print first page only
first_page = sites[:page_size]  # Simpler slice notation when starting from beginning
console_print(f"\nPage 1 of {total_pages}:")
console_print(json.dumps(first_page, indent=2))

# Print URLs for remaining pages without fetching data
for page in range(2, total_pages + 1):
    next_page_url = f"{SITE_HEALTH_URL}?page={page}&size={page_size}"
    console_print(f"\nURL for page {page}: {next_page_url}")

if response.status_code == 200:
    site_response = response.json()['response']
    for site in site_response:
        console_print(f"{site['siteName']}: {site['networkHealthWireless']}")
else:
    console_print(response.status_code, response.text)
