# trunk-ignore-all(isort)
"""Module providing a function printing python version."""
import sys
import os
import time
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import yaml
from dotenv import load_dotenv
from rich import print as console_print

# Load environment variables from .env file
load_dotenv()

# Get environment variables
username = os.getenv("DNAC_USERNAME")
password = os.getenv("DNAC_PASSWORD")

# Disable SSL warnings
urllib3.disable_warnings()


class DNACenterClientHealth:
    """Initializes a new DNAClientHealth object.

    Sets up the base URL, authentication URL, username, password, and initializes
    the token to None.
    """

    def __init__(self):
        self.base_url = "https://sandboxdnac2.cisco.com/dna"
        self.auth_url = "/system/api/v1/auth/token"
        self.username = username
        self.password = password
        self.token = None

    def get_auth_token(self):
        """Authenticate with DNA Center and get token"""
        try:
            response = requests.post(
                url=f"{self.base_url}{self.auth_url}",
                auth=HTTPBasicAuth(self.username, self.password),
                verify=False, # nosec
                timeout=30,
            )
            response.raise_for_status()
            self.token = response.json()["Token"]
            return self.token
        except requests.exceptions.RequestException as e:
            console_print(f"Error getting authentication token: {e}")
            sys.exit(1)

    def get_client_health(self):
        """Get client health statistics with retry mechanism"""
        if not self.token:
            self.get_auth_token()

        headers = {"X-Auth-Token": self.token, "Content-Type": "application/json"}

        client_health_url = f"{self.base_url}/intent/api/v1/client-health"
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url=client_health_url, headers=headers, verify=False, timeout=30
                ) # nosec
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                error_details = f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}"
                console_print(error_details)
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                console_print(f"Final error details: {type(e).__name__} - {str(e)}")
                return None

    def get_wireless_score(self, client_health):
        """Get wireless score from client health statistics"""
        for site in client_health.get("response", []):
            for detail in site.get("scoreDetail", []):
                if detail["scoreCategory"].get("value") == "WIRELESS":
                    return detail.get("scoreValue", "No scoreVlaue found")
        return "No WIRELESS category found"


def main():
    """Main function to get client health statistics"""
    dnac = DNACenterClientHealth()
    if client_health := dnac.get_client_health():
        console_print("\nClient Health Statistics:")
        # print(json.dumps(client_health, indent=2))
        console_print(yaml.dump(client_health, default_flow_style=False, sort_keys=False))
        # Get and print the WIRELESS score
        wireless_score = dnac.get_wireless_score(client_health)
        console_print(f"\n [bold yellow]WIRELESS Score: {wireless_score}[/bold yellow] \n")
    else:
        console_print("Failed to retrieve client health data")


if __name__ == "__main__":
    main()
