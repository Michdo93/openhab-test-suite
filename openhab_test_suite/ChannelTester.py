import json
from openhab import OpenHABClient, Links


class ChannelTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ChannelTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.links = Links(client)

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

    def isItemLinkedToChannel(self, itemName: str, channelUID: str) -> bool:
        """
        Checks if an item is linked to a specific channel.

        :param itemName: The name of the item.
        :param channelUID: The UID of the channel.
        :return: True if the link exists, False otherwise.
        """
        link = self._parseResponse(self.links.getLink(itemName, channelUID))
        return link is not None and link.get("itemName") == itemName

    def getLinksForItem(self, itemName: str) -> list:
        """
        Returns all channel links for a given item.

        :param itemName: The name of the item.
        :return: A list of link objects.
        """
        return self._parseListResponse(self.links.getLinks(itemName=itemName))

    def hasOrphanedLinks(self) -> bool:
        """
        Checks if there are any orphaned links (links pointing to non-existent channels).

        :return: True if orphaned links exist, False otherwise.
        """
        orphans = self._parseListResponse(self.links.getOrphanLinks())
        return len(orphans) > 0

    def isItemLinkedToAnyChannel(self, itemName: str) -> bool:
        """
        Checks if an item is linked to at least one channel.

        :param itemName: The name of the item.
        :return: True if the item has at least one channel link, False otherwise.
        """
        return len(self.getLinksForItem(itemName)) > 0
