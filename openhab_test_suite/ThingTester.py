import json
from openhab import OpenHABClient, Things


class ThingTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ThingTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.thingsAPI = Things(client)

    def _parseResponse(self, raw) -> dict:
        """Safely parse a raw API response to a dict."""
        if raw is None:
            return {}
        if isinstance(raw, dict):
            return raw
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}

    def _getThingStatus(self, thingUID: str) -> str:
        """
        Retrieves the status of a Thing based on its UID.

        :param thingUID: The unique identifier (UID) of the Thing.
        :return: The status string (e.g. "ONLINE", "OFFLINE"). Returns "UNKNOWN" if not determinable.
        """
        thing = self._parseResponse(self.thingsAPI.getThing(thingUID))
        if thing:
            statusInfo = thing.get("statusInfo", {})
            return statusInfo.get("status", "UNKNOWN")
        return "UNKNOWN"

    def isThingStatus(self, thingUID: str, statusToCheck: str) -> bool:
        """
        Checks whether a Thing has the specified status.

        :param thingUID: The unique identifier (UID) of the Thing.
        :param statusToCheck: The status to check against (e.g. "ONLINE", "OFFLINE").
        :return: True if the Thing has the specified status, False otherwise.
        """
        return self._getThingStatus(thingUID) == statusToCheck

    def isThingOnline(self, thingUID: str) -> bool:
        return self.isThingStatus(thingUID, "ONLINE")

    def isThingOffline(self, thingUID: str) -> bool:
        return self.isThingStatus(thingUID, "OFFLINE")

    def isThingPending(self, thingUID: str) -> bool:
        return self.isThingStatus(thingUID, "PENDING")

    def isThingUnknown(self, thingUID: str) -> bool:
        return self.isThingStatus(thingUID, "UNKNOWN")

    def isThingUninitialized(self, thingUID: str) -> bool:
        return self.isThingStatus(thingUID, "UNINITIALIZED")

    def isThingError(self, thingUID: str) -> bool:
        return self.isThingStatus(thingUID, "ERROR")

    def enableThing(self, thingUID: str) -> bool:
        """
        Enables a Thing.

        :param thingUID: The unique identifier (UID) of the Thing to be enabled.
        :return: True if the Thing was successfully enabled, False otherwise.
        """
        try:
            self.thingsAPI.setThingStatus(thingUID, True)
            print(f"Thing {thingUID} was successfully enabled.")
            return True
        except Exception as e:
            print(f"Error enabling thing {thingUID}: {e}")
            return False

    def disableThing(self, thingUID: str) -> bool:
        """
        Disables a Thing.

        :param thingUID: The unique identifier (UID) of the Thing to be disabled.
        :return: True if the Thing was successfully disabled, False otherwise.
        """
        try:
            self.thingsAPI.setThingStatus(thingUID, False)
            print(f"Thing {thingUID} was successfully disabled.")
            return True
        except Exception as e:
            print(f"Error disabling thing {thingUID}: {e}")
            return False
