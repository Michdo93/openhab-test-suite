from openhab import OpenHABClient, Persistence

class PersistenceTester:
    def __init__(self, client: OpenHABClient):
        self.client = client
        self.persistence = Persistence(client)

    def isItemPersisted(self, serviceID: str, itemName: str) -> bool:
            """Prüft ob ein Item in einem Persistence-Service vorhanden ist."""
            items = self.persistence.getItemsFromService(serviceID)
            
            # Da 'items' eine Liste von Strings ist, reicht ein einfaches 'in'
            return itemName in items

    def hasDataInRange(self, serviceID: str, itemName: str,
                       startTime: str, endTime: str) -> bool:
        """Prüft ob historische Daten im Zeitraum existieren."""
        data = self.persistence.getItemPersistenceData(
            serviceID, itemName, startTime, endTime
        )
        return data is not None and len(data.get("data", [])) > 0

    def checkLastPersistedState(self, serviceID: str, itemName: str,
                                 expectedState: str) -> bool:
        """Prüft ob der zuletzt persistierte Wert dem erwarteten entspricht."""
        data = self.persistence.getItemPersistenceData(serviceID, itemName)
        entries = data.get("data", [])
        if not entries:
            return False
        lastState = entries[-1].get("state")
        return str(lastState) == str(expectedState)