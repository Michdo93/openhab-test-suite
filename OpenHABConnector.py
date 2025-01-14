import requests
import json

class OpenHABConnector:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session = requests.Session()

        if self.username and self.password:
            self.auth = (self.username, self.password)
            self.session.auth = self.auth
        else:
            self.auth = None

        self.check_connection()

    def check_connection(self):
        """Überprüft die Verbindung zu OpenHAB."""
        try:
            response = self.session.get(f"{self.base_url}/rest", timeout=5)
            response.raise_for_status()
            print("Verbindung zu OpenHAB hergestellt.")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Verbinden mit OpenHAB: {e}")

    def get(self, endpoint):
        """Führt einen GET-Request durch."""
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei GET {endpoint}: {e}")
            return None

    def put(self, endpoint, data):
        """Führt einen PUT-Request durch."""
        try:
            response = self.session.put(f"{self.base_url}{endpoint}", data=json.dumps(data), timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei PUT {endpoint}: {e}")

    def post(self, endpoint, data):
        """Führt einen POST-Request durch."""
        try:
            response = self.session.post(f"{self.base_url}{endpoint}", data=json.dumps(data), timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei POST {endpoint}: {e}")

    def delete(self, endpoint):
        """Führt einen DELETE-Request durch."""
        try:
            response = self.session.delete(f"{self.base_url}{endpoint}", timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei DELETE {endpoint}: {e}")
