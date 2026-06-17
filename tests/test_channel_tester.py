from openhab_test_suite import ChannelTester
from openhab import OpenHABClient

# Establishing connection to the OpenHAB API
#client = OpenHABClient("http://127.0.0.1:8080", "openhab", "habopen")
client = OpenHABClient("http://192.168.0.5:8080", "openHABAdmin", "hJem2jz6")

# Instantiation of the ChannelTester
channelTester = ChannelTester(client)

# Replace with actual values from your openHAB instance.
# Example: an astro binding channel linked to an item.
itemName   = "testSwitch"
channelUID = "astro:moon:56bdb13645:phase#name"

print("=" * 60)
print("Testing ChannelTester")
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
# Check if a specific item is linked to a specific channel
# ------------------------------------------------------------------
print(f"\n--- Link check: '{itemName}' <-> '{channelUID}' ---")
check(
    f"isItemLinkedToChannel('{itemName}', '{channelUID}')",
    channelTester.isItemLinkedToChannel(itemName, channelUID),
)

# ------------------------------------------------------------------
# Get all channels linked to an item
# ------------------------------------------------------------------
print(f"\n--- All links for item '{itemName}' ---")
links = channelTester.getLinksForItem(itemName)
check(f"getLinksForItem('{itemName}')", links)
for link in links:
    print(f"  channelUID: {link.get('channelUID')}  |  config: {link.get('configuration')}")

# ------------------------------------------------------------------
# Check if the item is linked to at least one channel
# ------------------------------------------------------------------
print(f"\n--- Is item linked to any channel? ---")
check(
    f"isItemLinkedToAnyChannel('{itemName}')",
    channelTester.isItemLinkedToAnyChannel(itemName),
)

# ------------------------------------------------------------------
# Check for orphaned links (links pointing to non-existent channels)
# ------------------------------------------------------------------
print(f"\n--- Orphaned links ---")
check("hasOrphanedLinks()", channelTester.hasOrphanedLinks())

print("\n" + "=" * 60)
print("ChannelTester tests complete.")
print("=" * 60)