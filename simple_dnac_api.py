import requests
import json
from urllib3.exceptions import InsecureRequestWarning
from rich import print
import sys
args = sys.argv[1:]
from requests.exceptions import Timeout
import yaml

# ################################################# Disable warnings #################################################
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Base URL and Endpoint
base_url = "https://sandboxdnac2.cisco.com/dna/"
auth_url = "system/api/v1/auth/token"

# Get the Token
payload = ""
headers = {
    'content-type': 'application/json',
    'Authorization': "Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE="
}

response = requests.post(f"{base_url}{auth_url}", headers=headers, verify=False, timeout=30)
auth_token = response.json()['Token']
print(auth_token)


# #################################### Get the Network Health /intent/api/v1/network-health | category=Wireless ##########
endpoint_url = "intent/api/v1/network-health"

headers = {
    'content-type': 'application/json',
    'Accept': 'application/json',
    'x-auth-token': auth_token
}
response = requests.get(f"{base_url}{endpoint_url}", headers=headers, verify=False, timeout=30)
network_health = response.json()
print("\n[bold]Network Health\n")
print(json.dumps(network_health, indent=2))
# print(network_health)

# ##################category=Core | change the category to other if values are available | category=Wireless
print("\nCategory=Core\n")
for healthDist in network_health['healthDistirubution']:
    if healthDist['category'] == 'Core':
        print(json.dumps(healthDist, indent=2))
        break
    
#################### print goodCount, badCount, totalCount, healthScore under network-health[0]
print("\nGood Count, Bad Count, Total Count, Health Score\n")
if response.status_code == 200:
    network_health = response.json()['response']
    print('Good: {0}, Bad: {1}, Health Score: {2}'.format(network_health[0]['goodCount'], network_health[0]['badCount'], network_health[0]['healthScore']))
######################## Get the Site Health | /intent/api/v1/site-health   for networkHealthWireless #######################
# Get the Site Health | python simple_dnac_api.py "SiteName" | python simple_dnac_api.py "SanJose"
# replace 'networkHealthSwitch' with 'networkHealthWireless' if data is avilable
print("\n[bold]Site Health\n")
endpoint_url = "intent/api/v1/site-health"
response = requests.get(f"{base_url}{endpoint_url}", headers=headers, verify=False, timeout=30)
site_health = response.json()['response']
# print(json.dumps(site_health, indent=2)) # Uncomment to see the full response
############ networkHealthWireless ############################
for site in site_health:
    if site['siteName'] == args[0]:
        if site['networkHealthSwitch'] > 90:
            print(f"{site['siteName']} site wirelss health is " f"{site['networkHealthSwitch']}; needs attention!")     
########################################### Error handling #############################################
print("\n[bold red]Error Handling\n")
dnac_url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/network_health" # Change the URL to see the error handling
sess = requests.session()
try:
    rc = sess.request('GET', dnac_url, headers=headers, timeout=30, verify=False) # nosec | reduce the timeout value to see the Timeout error
except Timeout:
    print('TIMEOUT ERROR: Unable to access DNA Center!')
    exit(-1)
if rc.status_code == requests.codes['ok']:
    print('The request was successful!')
else:
    print(f'Error Code: {rc.status_code} : {rc.reason}')
################# client-health | /intent/api/v1/cleint-health for scoreCategory WIRELESS #######################

print("\n[bold]Client Health\n")
"""
endpoint_url = "intent/api/v1/client-health"
response = requests.get(f"{base_url}{endpoint_url}", headers=headers, verify=False, timeout=30) # nosec
Extract wireless client health stats
client_health = response.json()
Load the local YAML file
"""

## Testing with saved client-health in yaml file
yaml_file = 'client-health.yaml'
with open(yaml_file, 'r') as file:
    client_health = yaml.safe_load(file)

# print(json.dumps(client_health, indent=2)) # Uncomment to see the full response
wireless_health_stats = [
    score['clientUniqueCount']
    for score_detail in client_health['response'][0]['scoreDetail']
    if score_detail['scoreCategory']['value'] == 'WIRELESS'
    for score in score_detail.get('scoreList', [])
    if score['scoreCategory']['value'] == 'POOR'
]
print("Wireless Health Stats (POOR):", wireless_health_stats)