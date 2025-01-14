class ThingTester:
    def __init__(self, connector):
        self.connector = connector

    def get_thing_status(self, thing_uid):
        """Ruft den Status eines Things ab."""
        endpoint = f"/rest/things/{thing_uid}"
        response = self.connector.get(endpoint)
        if response:
            status_info = response.get("statusInfo", {})
            status = status_info.get("status", "UNKNOWN")
            print(f"Thing {thing_uid} Status: {status}")
            return status
        return None

    def is_thing_in_status(self, thing_uid, status_to_check):
        """Prüft, ob ein Thing einen bestimmten Status hat."""
        current_status = self.get_thing_status(thing_uid)
        return current_status == status_to_check

    def is_thing_online(self, thing_uid):
        """Prüft, ob ein Thing ONLINE ist."""
        return self.is_thing_in_status(thing_uid, "ONLINE")

    def is_thing_offline(self, thing_uid):
        """Prüft, ob ein Thing OFFLINE ist."""
        return self.is_thing_in_status(thing_uid, "OFFLINE")

    def is_thing_pending(self, thing_uid):
        """Prüft, ob ein Thing PENDING ist."""
        return self.is_thing_in_status(thing_uid, "PENDING")

    def is_thing_unknown(self, thing_uid):
        """Prüft, ob ein Thing UNKNOWN ist."""
        return self.is_thing_in_status(thing_uid, "UNKNOWN")

    def is_thing_uninitialized(self, thing_uid):
        """Prüft, ob ein Thing UNINITIALIZED ist."""
        return self.is_thing_in_status(thing_uid, "UNINITIALIZED")

    def is_thing_error(self, thing_uid):
        """Prüft, ob ein Thing ERROR ist."""
        return self.is_thing_in_status(thing_uid, "ERROR")
