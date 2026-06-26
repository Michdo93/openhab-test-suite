import json
from openhab import OpenHABClient, Sitemaps


class SitemapTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the SitemapTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.sitemaps = Sitemaps(client)

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

    def doesSitemapExist(self, sitemapName: str) -> bool:
        """
        Checks if a sitemap with the given name exists.

        :param sitemapName: The name of the sitemap.
        :return: True if the sitemap exists, False otherwise.
        """
        all_sitemaps = self._parseListResponse(self.sitemaps.getSitemaps())
        return any(s.get("name") == sitemapName for s in all_sitemaps)

    def doesSitemapContainItem(self, sitemapName: str, itemName: str) -> bool:
        """
        Checks if an item is referenced anywhere inside a sitemap.

        :param sitemapName: The name of the sitemap.
        :param itemName: The name of the item to search for.
        :return: True if the item appears in the sitemap, False otherwise.
        """
        sitemap = self._parseResponse(self.sitemaps.getSitemap(sitemapName))
        return self._searchForItem(sitemap, itemName)

    def _searchForItem(self, node, itemName: str) -> bool:
        """
        Recursively searches for an item name in a sitemap node tree.

        :param node: The current node to search (dict, list, or scalar).
        :param itemName: The item name to find.
        :return: True if found, False otherwise.
        """
        if isinstance(node, dict):
            if node.get("item", {}).get("name") == itemName:
                return True
            for value in node.values():
                if self._searchForItem(value, itemName):
                    return True
        elif isinstance(node, list):
            for element in node:
                if self._searchForItem(element, itemName):
                    return True
        return False
