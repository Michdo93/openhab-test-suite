from openhab import OpenHABClient, Sitemaps

class SitemapTester:
    def __init__(self, client: OpenHABClient):
        self.client = client
        self.sitemaps = Sitemaps(client)

    def doesSitemapExist(self, sitemapName: str) -> bool:
        all_sitemaps = self.sitemaps.getSitemaps()
        return any(s.get("name") == sitemapName for s in all_sitemaps)

    def doesSitemapContainItem(self, sitemapName: str, itemName: str) -> bool:
        """Prüft ob ein Item irgendwo in der Sitemap referenziert wird."""
        sitemap = self.sitemaps.getSitemap(sitemapName)
        return self._searchForItem(sitemap, itemName)

    def _searchForItem(self, node: dict, itemName: str) -> bool:
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