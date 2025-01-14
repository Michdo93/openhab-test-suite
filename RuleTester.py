import time
from OpenHABConnector import OpenHABConnector
import json

class RuleTester:
    def __init__(self, connector: OpenHABConnector):
        self.connector = connector

    def run_rule(self, rule_uid: str) -> bool:
        """Führt eine Regel sofort aus."""
        endpoint = f"/rules/{rule_uid}/runnow"
        # JSON-Daten senden
        data = {}  # Füge hier die notwendigen Daten ein, falls erforderlich
        response = self.connector.post(endpoint, headers={"Content-type": "application/json", "Accept": "application/json"}, data=json.dumps(data))

        if response and response.status_code == 200:
            print(f"Regel {rule_uid} erfolgreich ausgeführt.")
            return True
        print(f"Fehler beim Ausführen der Regel {rule_uid}. Antwort: {response}")
        return False

    def enable_rule(self, rule_uid: str) -> bool:
        """Aktiviert eine Regel."""
        endpoint = f"/rules/{rule_uid}/enable"
        # Keine Daten für PUT erforderlich, aber korrekt als JSON senden
        response = self.connector.put(endpoint, headers={"Content-type": "application/json", "Accept": "application/json"})

        if response and response.status_code == 200:
            print(f"Regel {rule_uid} erfolgreich aktiviert.")
            return True
        print(f"Fehler beim Aktivieren der Regel {rule_uid}. Antwort: {response}")
        return False

    def disable_rule(self, rule_uid: str) -> bool:
        """Deaktiviert eine Regel."""
        endpoint = f"/rules/{rule_uid}/disable"
        response = self.connector.put(endpoint, headers={"Content-type": "application/json", "Accept": "application/json"})

        if response and response.status_code == 200:
            print(f"Regel {rule_uid} erfolgreich deaktiviert.")
            return True
        print(f"Fehler beim Deaktivieren der Regel {rule_uid}. Antwort: {response}")
        return False

    def test_rule_execution(self, rule_uid: str, expected_item: str, expected_value: str) -> bool:
        """
        Testet die Ausführung einer Regel und verifiziert das erwartete Ergebnis.

        :param rule_uid: Die UID der Regel.
        :param expected_item: Das zu prüfende Item nach der Regel-Ausführung.
        :param expected_value: Der erwartete Wert des Items.
        :return: True, wenn der Test erfolgreich war, andernfalls False.
        """
        try:
            # Regel ausführen
            if not self.run_rule(rule_uid):
                print(f"Fehler: Regel {rule_uid} konnte nicht ausgeführt werden.")
                return False

            # Kurze Pause für die Regel-Ausführung
            time.sleep(2)

            # Zustand des Items abrufen
            state = self.connector.get(f"/items/{expected_item}/state")
            if state is None or state != expected_value:
                print(f"Fehler: Zustand des Items {expected_item} nach der Regel-Ausführung stimmt nicht überein. Erwartet: {expected_value}, Gefunden: {state}")
                return False

            print(f"{expected_item} Zustand nach der Regel-Ausführung: {state}")
            return state == expected_value
        except Exception as e:
            print(f"Fehler bei der Regel-Testausführung: {e}")
            return False
