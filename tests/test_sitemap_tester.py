from openhab_test_suite import SitemapTester
from openhab import OpenHABClient

# Establishing connection to the OpenHAB API
#client = OpenHABClient("http://127.0.0.1:8080", "openhab", "habopen")
client = OpenHABClient("http://192.168.0.5:8080", "openHABAdmin", "hJem2jz6")

# Instantiation of the SitemapTester
sitemapTester = SitemapTester(client)

# Replace with actual values from your openHAB instance.
sitemapName     = "default"     # name of the sitemap to test
existingItem    = "testSwitch"  # an item that is referenced in the sitemap
nonExistingItem = "itemThatDoesNotExist"  # should NOT be found in the sitemap

print("=" * 60)
print("Testing SitemapTester")
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
# Check if the sitemap exists at all
# ------------------------------------------------------------------
print(f"\n--- Sitemap existence ---")
check(
    f"doesSitemapExist('{sitemapName}')",
    sitemapTester.doesSitemapExist(sitemapName),
)

# Also verify that a non-existent sitemap returns False
check(
    "doesSitemapExist('nonExistingSitemap')",
    sitemapTester.doesSitemapExist("nonExistingSitemap"),
)

# ------------------------------------------------------------------
# Check if known items are referenced inside the sitemap
# ------------------------------------------------------------------
print(f"\n--- Item references in sitemap '{sitemapName}' ---")
check(
    f"doesSitemapContainItem('{sitemapName}', '{existingItem}')",
    sitemapTester.doesSitemapContainItem(sitemapName, existingItem),
)

check(
    f"doesSitemapContainItem('{sitemapName}', '{nonExistingItem}')",
    sitemapTester.doesSitemapContainItem(sitemapName, nonExistingItem),
)

print("\n" + "=" * 60)
print("SitemapTester tests complete.")
print("=" * 60)