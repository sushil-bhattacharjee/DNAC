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

# Get the token
response = requests.post(url=f"{base_url}{endpoint_url}", headers=headers, data=payload, verify=False)

try:
    response_json = response.json()
except requests.exceptions.JSONDecodeError as e:
    print(f"[red]Failed to parse JSON: {e}[/red]")
    exit(1)

Token = response_json.get('Token')
if not Token:
    print("[red]Token not found! Exiting.[/red]")
    exit(1)

print(f"[green]Token acquired: {Token}[/green]")

####################### Get Client Health ###################
req_headers = {
    'content-type': 'application/json',
    'Accept': 'application/json',
    'x-auth-token': Token
}

url = "https://10.10.20.85/dna/intent/api/v1"
endpoint = "/client-health"

# Fetch client health
response_clienthealth = requests.get(url=f"{url}{endpoint}", headers=req_headers, verify=False)
if response_clienthealth.status_code != 200:
    print(f"[red]Failed to fetch client health! HTTP {response_clienthealth.status_code}[/red]")
    exit(1)

try:
    client_health = response_clienthealth.json()
    print("\n[red]Printing ALL the client-health raw Data in JSON format\n")
    print(json.dumps(client_health, indent=2))
except requests.exceptions.JSONDecodeError as e:
    print(f"[red]Failed to parse Client Health JSON: {e}[/red]")
    exit(1)

####################### Process and Print Health Scores ###################
print("\n[yellow]Client Health Scores:[/yellow]\n")

if 'response' in client_health and len(client_health['response']) > 0:
    score_details = client_health['response'][0].get('scoreDetail', [])

    for score in score_details:
        client_type = score['scoreCategory']['value']  # ALL, WIRED, WIRELESS
        client_count = score.get('clientCount', 0)

        print(f"[green]Client Type:[/green] {client_type} [blue]Client Count:[/blue] {client_count}")

        # Process scoreList if it exists
        score_list = score.get('scoreList', [])
        if score_list:
            print(f"  [yellow]Score Breakdown for {client_type}:[/yellow]")
            for detail in score_list:
                score_value = detail['scoreCategory']['value']  # POOR, FAIR, GOOD, etc.
                count = detail.get('clientCount', 0)
                print(f"    {score_value}: {count}")
else:
    print("[red]No client health data found.[/red]")

