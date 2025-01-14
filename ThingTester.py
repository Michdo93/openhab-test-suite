from OpenHABConnector import OpenHABConnector

class ThingTester:
    def __init__(self, connector: OpenHABConnector):
        self.connector = connector

    def _get_thing_status(self, thing_uid: str) -> str:
        """Holt den Status eines Things."""
        endpoint = f"/rest/things/{thing_uid}"
        response = self.connector.get(endpoint)
        if response:
            status_info = response.get("statusInfo", {})
            return status_info.get("status", "UNKNOWN")
        return "UNKNOWN"

    def is_thing_status(self, thing_uid: str, status_to_check: str) -> bool:
        """Prüft, ob ein Thing den angegebenen Status hat."""
        return self._get_thing_status(thing_uid) == status_to_check

    def is_thing_online(self, thing_uid: str) -> bool:
        """Prüft, ob ein Thing ONLINE ist."""
        return self.is_thing_status(thing_uid, "ONLINE")

    def is_thing_offline(self, thing_uid: str) -> bool:
        """Prüft, ob ein Thing OFFLINE ist."""
        return self.is_thing_status(thing_uid, "OFFLINE")

    def is_thing_pending(self, thing_uid: str) -> bool:
        """Prüft, ob ein Thing PENDING ist."""
        return self.is_thing_status(thing_uid, "PENDING")

    def is_thing_unknown(self, thing_uid: str) -> bool:
        """Prüft, ob ein Thing UNKNOWN ist."""
        return self.is_thing_status(thing_uid, "UNKNOWN")

    def is_thing_uninitialized(self, thing_uid: str) -> bool:
        """Prüft, ob ein Thing UNINITIALIZED ist."""
        return self.is_thing_status(thing_uid, "UNINITIALIZED")

    def is_thing_error(self, thing_uid: str) -> bool:
        """Prüft, ob ein Thing ERROR ist."""
        return self.is_thing_status(thing_uid, "ERROR")
