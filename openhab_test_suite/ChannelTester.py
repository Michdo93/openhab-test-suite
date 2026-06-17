from openhab import OpenHABClient, Links

class ChannelTester:
    def __init__(self, client: OpenHABClient):
        self.client = client
        self.links = Links(client)

    def isItemLinkedToChannel(self, itemName: str, channelUID: str) -> bool:
        link = self.links.getLink(itemName, channelUID)
        return link is not None and link.get("itemName") == itemName

    def getLinksForItem(self, itemName: str) -> list:
        all_links = self.links.getLinks(itemName=itemName)
        return all_links if all_links else []

    def hasOrphanedLinks(self) -> bool:
        orphans = self.links.getOrphanLinks()
        return len(orphans) > 0

    def isItemLinkedToAnyChannel(self, itemName: str) -> bool:
        return len(self.getLinksForItem(itemName)) > 0