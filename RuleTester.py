class RuleTester:
    def __init__(self, connector):
        self.connector = connector

    def get_rule_status(self, rule_uid):
        """Ruft den Status einer Regel ab."""
        endpoint = f"/rest/rules/{rule_uid}/status"
        response = self.connector.get(endpoint)
        if response:
            status = response.get("status", "UNKNOWN")
            print(f"Rule {rule_uid} Status: {status}")
            return status
        return None

    def is_rule_active(self, rule_uid):
        """Prüft, ob eine Regel aktiv (IDLE oder RUNNING) ist."""
        status = self.get_rule_status(rule_uid)
        return status in ["IDLE", "RUNNING"]

    def is_rule_idle(self, rule_uid):
        """Prüft, ob eine Regel im Status IDLE ist."""
        return self.get_rule_status(rule_uid) == "IDLE"

    def is_rule_running(self, rule_uid):
        """Prüft, ob eine Regel gerade ausgeführt wird (RUNNING)."""
        return self.get_rule_status(rule_uid) == "RUNNING"

    def is_rule_disabled(self, rule_uid):
        """Prüft, ob eine Regel deaktiviert ist."""
        return self.get_rule_status(rule_uid) == "DISABLED"

    def enable_rule(self, rule_uid):
        """Aktiviert eine Regel."""
        endpoint = f"/rest/rules/{rule_uid}/enable"
        response = self.connector.put(endpoint)
        if response is None:
            print(f"Rule {rule_uid} erfolgreich aktiviert.")
            return True
        print(f"Fehler beim Aktivieren der Regel {rule_uid}.")
        return False

    def disable_rule(self, rule_uid):
        """Deaktiviert eine Regel."""
        endpoint = f"/rest/rules/{rule_uid}/disable"
        response = self.connector.put(endpoint)
        if response is None:
            print(f"Rule {rule_uid} erfolgreich deaktiviert.")
            return True
        print(f"Fehler beim Deaktivieren der Regel {rule_uid}.")
        return False

    def run_rule(self, rule_uid):
        """Führt eine Regel manuell aus."""
        endpoint = f"/rest/rules/{rule_uid}/run"
        response = self.connector.post(endpoint)
        if response is None:
            print(f"Rule {rule_uid} erfolgreich ausgeführt.")
            return True
        print(f"Fehler beim Ausführen der Regel {rule_uid}.")
        return False
