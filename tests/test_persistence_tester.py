from openhab_test_suite import PersistenceTester
from openhab import OpenHABClient

# Establishing connection to the OpenHAB API
#client = OpenHABClient("http://127.0.0.1:8080", "openhab", "habopen")
client = OpenHABClient("http://192.168.0.5:8080", "openHABAdmin", "hJem2jz6")

# Instantiation of the PersistenceTester
persistenceTester = PersistenceTester(client)

# Replace with actual values from your openHAB instance.
serviceID  = "rrd4j"       # e.g. "rrd4j", "mapdb", "influxdb"
itemName   = "testSwitch"  # an item that is actually persisted

# Time range for historical data checks (ISO-8601)
startTime  = "2025-01-01T00:00:00.000Z"
endTime    = "2025-12-31T23:59:59.999Z"

# A state value you expect to find as the latest persisted entry
expectedLastState = "ON"

print("=" * 60)
print("Testing PersistenceTester")
print("=" * 60)

# ------------------------------------------------------------------
# Helper: print result uniformly
# ------------------------------------------------------------------
def check(label: str, result):
    if isinstance(result, bool):
        status = "OK" if result else "FAIL"
        print(f"[{status}] {label}: {result}")
    else:
        print(f"[INFO] {label}: {result}")

# ------------------------------------------------------------------
# Check if the item is registered in the persistence service at all
# ------------------------------------------------------------------
print(f"\n--- Is item persisted? ---")
check(
    f"isItemPersisted(serviceID='{serviceID}', itemName='{itemName}')",
    persistenceTester.isItemPersisted(serviceID, itemName),
)

# ------------------------------------------------------------------
# Check if historical data exists in a given time range
# ------------------------------------------------------------------
print(f"\n--- Historical data in range ---")
check(
    f"hasDataInRange('{itemName}', {startTime} -> {endTime})",
    persistenceTester.hasDataInRange(serviceID, itemName, startTime, endTime),
)

# ------------------------------------------------------------------
# Check the last persisted state
# ------------------------------------------------------------------
print(f"\n--- Last persisted state ---")
check(
    f"checkLastPersistedState('{itemName}', expectedState='{expectedLastState}')",
    persistenceTester.checkLastPersistedState(serviceID, itemName, expectedLastState),
)

print("\n" + "=" * 60)
print("PersistenceTester tests complete.")
print("=" * 60)