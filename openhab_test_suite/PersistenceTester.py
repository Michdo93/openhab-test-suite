import json
from openhab import OpenHABClient, Persistence


class PersistenceTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the PersistenceTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.persistence = Persistence(client)

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

    def _parseListResponse(self, raw) -> list:
        """Safely parse a raw API response to a list."""
        if raw is None:
            return []
        if isinstance(raw, list):
            return raw
        try:
            result = json.loads(raw)
            return result if isinstance(result, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def isItemPersisted(self, serviceID: str, itemName: str) -> bool:
        """
        Checks if an item is registered in a persistence service.

        :param serviceID: The ID of the persistence service (e.g. "rrd4j").
        :param itemName: The name of the item to check.
        :return: True if the item is persisted, False otherwise.
        """
        raw = self.persistence.getItemsFromService(serviceID)
        # getItemsFromService returns a list of dicts with a "name" field
        items = self._parseListResponse(raw)
        return any(
            (entry.get("name") == itemName if isinstance(entry, dict) else entry == itemName)
            for entry in items
        )

    def hasDataInRange(self, serviceID: str, itemName: str,
                       startTime: str, endTime: str) -> bool:
        """
        Checks if historical data exists for an item within a given time range.

        :param serviceID: The ID of the persistence service.
        :param itemName: The name of the item.
        :param startTime: Start of the time range (ISO-8601).
        :param endTime: End of the time range (ISO-8601).
        :return: True if data points exist in the range, False otherwise.
        """
        # BUG FIX: parameter order is itemName, serviceID (not serviceID, itemName)
        raw = self.persistence.getItemPersistenceData(
            itemName, serviceID, startTime, endTime
        )
        data = self._parseResponse(raw)
        return data is not None and len(data.get("data", [])) > 0

    def checkLastPersistedState(self, serviceID: str, itemName: str,
                                 expectedState: str) -> bool:
        """
        Checks if the most recently persisted value of an item matches the expected state.

        :param serviceID: The ID of the persistence service.
        :param itemName: The name of the item.
        :param expectedState: The expected state value.
        :return: True if the last persisted state matches, False otherwise.
        """
        # BUG FIX: parameter order is itemName, serviceID (not serviceID, itemName)
        raw = self.persistence.getItemPersistenceData(itemName, serviceID)
        data = self._parseResponse(raw)
        entries = data.get("data", [])
        if not entries:
            return False
        lastState = entries[-1].get("state")
        return str(lastState) == str(expectedState)
