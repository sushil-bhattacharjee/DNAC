import yaml
import json
from rich import print

# # Load the YAML data from the file
# with open("client-health.yaml", "r") as file:
#     client_health = yaml.safe_load(file)

# Load the JSON data from the file
with open("client_health.json", "r") as file:
    client_health = json.load(file)

# Process and print the summary
print("\n[yellow]Client Health Scores:[/yellow]\n")

# Ensure response data exists
if "response" in client_health and len(client_health["response"]) > 0:
    score_details = client_health["response"][0].get("scoreDetail", [])

    # Loop through each client type (ALL, WIRED, WIRELESS)
    for score in score_details:
        client_type = score["scoreCategory"]["value"]  # ALL, WIRED, WIRELESS
        client_count = score.get("clientCount", 0)

        print(f"[green]Client Type:[/green] {client_type} [blue]Client Count:[/blue] {client_count}")

        # Process score breakdown (POOR, FAIR, GOOD, etc.)
        score_list = score.get("scoreList", [])
        if score_list:
            print(f"  [yellow]Score Breakdown for {client_type}:[/yellow]")
            for detail in score_list:
                score_value = detail["scoreCategory"]["value"]  # POOR, FAIR, GOOD, etc.
                count = detail.get("clientCount", 0)
                print(f"    {score_value}: {count}")
else:
    print("[red]No client health data found.[/red]")
