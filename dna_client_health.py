import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
import sys

# Disable SSL warnings
urllib3.disable_warnings()

class DNACenterClientHealth:
    def __init__(self):
        self.base_url = "https://sandboxdnac2.cisco.com/dna"
        self.auth_url = "/system/api/v1/auth/token"
        self.username = "devnetuser"
        self.password = "Cisco123!"
        self.token = None

    def get_auth_token(self):
        """Authenticate with DNA Center and get token"""
        try:
            response = requests.post(
                url=f"{self.base_url}{self.auth_url}",
                auth=HTTPBasicAuth(self.username, self.password),
                verify=False
            )
            response.raise_for_status()
            self.token = response.json()["Token"]
            return self.token
        except requests.exceptions.RequestException as e:
            print(f"Error getting authentication token: {e}")
            sys.exit(1)

    def get_client_health(self):
        """Get client health statistics"""
        if not self.token:
            self.get_auth_token()

        headers = {
            "X-Auth-Token": self.token,
            "Content-Type": "application/json"
        }

        client_health_url = f"{self.base_url}/intent/api/v1/client-health"

        try:
            response = requests.get(
                url=client_health_url,
                headers=headers,
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting client health: {e}")
            return None

def main():
    dnac = DNACenterClientHealth()
    
    # Get client health data
    client_health = dnac.get_client_health()
    
    if client_health:
        print("\nClient Health Statistics:")
        print(json.dumps(client_health, indent=2))
    else:
        print("Failed to retrieve client health data")

if __name__ == "__main__":
    main() 