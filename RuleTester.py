import time
from OpenHABConnector import OpenHABConnector

class RuleTester:
    def __init__(self, connector: OpenHABConnector):
        self.connector = connector

    def _get_status(self, rule_uid: str) -> str:
        """Ruft den Status einer Regel ab."""
        endpoint = f"/rest/rules/{rule_uid}/status"
        response = self.connector.get(endpoint)
        if response:
            return response.get("status", "UNKNOWN")
        return "UNKNOWN"

    def is_rule_status(self, rule_uid: str, status_to_check: str) -> bool:
        """Prüft, ob eine Regel einen bestimmten Status hat."""
        return self._get_status(rule_uid) == status_to_check

    def is_rule_active(self, rule_uid: str) -> bool:
        """Prüft, ob eine Regel aktiv (IDLE oder RUNNING) ist."""
        return self.is_rule_status(rule_uid, "IDLE") or self.is_rule_status(rule_uid, "RUNNING")

    def enable_rule(self, rule_uid: str) -> bool:
        """Aktiviert eine Regel."""
        endpoint = f"/rest/rules/{rule_uid}/enable"
        return self._toggle_rule(endpoint, rule_uid)

    def disable_rule(self, rule_uid: str) -> bool:
        """Deaktiviert eine Regel."""
        endpoint = f"/rest/rules/{rule_uid}/disable"
        return self._toggle_rule(endpoint, rule_uid)

    def _toggle_rule(self, endpoint: str, rule_uid: str) -> bool:
        """Hilfsmethode zum Aktivieren/Deaktivieren einer Regel."""
        response = self.connector.put(endpoint)
        if response is None:
            print(f"Rule {rule_uid} erfolgreich geändert.")
            return True
        print(f"Fehler beim Ändern der Regel {rule_uid}.")
        return False

    def run_rule(self, rule_uid: str) -> bool:
        """Führt eine Regel manuell aus."""
        endpoint = f"/rest/rules/{rule_uid}/run"
        response = self.connector.post(endpoint)
        if response is None:
            print(f"Rule {rule_uid} erfolgreich ausgeführt.")
            return True
        print(f"Fehler beim Ausführen der Regel {rule_uid}.")
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
            self.run_rule(rule_uid)
            time.sleep(2)
            state = self.connector.get(f"/rest/items/{expected_item}/state")
            print(f"{expected_item} state after rule execution: {state}")
            return state == expected_value
        except Exception as e:
            print(f"Fehler bei der Regel-Testausführung: {e}")
            return False
