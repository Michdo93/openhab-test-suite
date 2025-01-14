# test_thing_tester.py
import time
from OpenHABConnector import OpenHABConnector
from ThingTester import ThingTester

# Hier stellen wir die Verbindung zur OpenHAB API her
connector = OpenHABConnector("http://localhost:8080", "openhab", "habopen")

# Instanziierung des ThingTesters
thing_tester = ThingTester(connector)

# Beispiel: Testen der verschiedenen Status eines Things
thing_uid = "exampleThingUid"  # Ersetze dies mit der echten Thing-UID

print("Testing ThingTester...")

# Teste, ob das Thing ONLINE ist
if thing_tester.is_thing_online(thing_uid):
    print(f"Thing {thing_uid} ist ONLINE.")
else:
    print(f"Thing {thing_uid} ist NICHT ONLINE.")

# Teste, ob das Thing OFFLINE ist
if thing_tester.is_thing_offline(thing_uid):
    print(f"Thing {thing_uid} ist OFFLINE.")
else:
    print(f"Thing {thing_uid} ist NICHT OFFLINE.")

# Teste, ob das Thing ERROR ist
if thing_tester.is_thing_error(thing_uid):
    print(f"Thing {thing_uid} hat einen Fehler.")
else:
    print(f"Thing {thing_uid} hat keinen Fehler.")

# Teste, ob das Thing im Status PENDING ist
if thing_tester.is_thing_pending(thing_uid):
    print(f"Thing {thing_uid} ist im Status PENDING.")
else:
    print(f"Thing {thing_uid} ist NICHT im Status PENDING.")
