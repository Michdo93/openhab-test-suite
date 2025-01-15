# test_thing_tester.py
import time
from OpenHABConnector import OpenHABConnector
from ThingTester import ThingTester

# Here we establish the connection to the OpenHAB API
connector = OpenHABConnector("http://127.0.0.1:8080", "openhab", "habopen")

# Instantiation of the ThingTester
thing_tester = ThingTester(connector)

# Example: Testing the various statuses of a Thing
thing_uid = "astro:moon:56bdb13645"  # Replace with the actual Thing UID
thing_uid2 = "astro:sun:560560e11a"  # Replace with the actual Thing UID

"""
curl -u openhab:habopen -X PUT -H "Content-Type: text/plain" --data "true" http://127.0.0.1:8080/rest/things/astro:moon:56bdb13645/enable
curl -u openhab:habopen -X PUT -H "Content-Type: text/plain" --data "false" http://127.0.0.1:8080/rest/things/astro:moon:56bdb13645/enable
"""

print("Testing ThingTester...")

# Test if the Thing is ONLINE
if thing_tester.is_thing_online(thing_uid):
    print(f"Thing {thing_uid} is ONLINE.")
else:
    print(f"Thing {thing_uid} is NOT ONLINE.")

# Test if the Thing is OFFLINE
if thing_tester.is_thing_offline(thing_uid):
    print(f"Thing {thing_uid} is OFFLINE.")
else:
    print(f"Thing {thing_uid} is NOT OFFLINE.")

# Test if the Thing is in ERROR state
if thing_tester.is_thing_error(thing_uid):
    print(f"Thing {thing_uid} has an error.")
else:
    print(f"Thing {thing_uid} has no error.")

# Test if the Thing is in PENDING state
if thing_tester.is_thing_pending(thing_uid):
    print(f"Thing {thing_uid} is in PENDING state.")
else:
    print(f"Thing {thing_uid} is NOT in PENDING state.")

# Test the second Thing
if thing_tester.is_thing_online(thing_uid2):
    print(f"Thing {thing_uid2} is ONLINE.")
else:
    print(f"Thing {thing_uid2} is NOT ONLINE.")

# Test if the second Thing is OFFLINE
if thing_tester.is_thing_offline(thing_uid2):
    print(f"Thing {thing_uid2} is OFFLINE.")
else:
    print(f"Thing {thing_uid2} is NOT OFFLINE.")

# Test if the second Thing is in ERROR state
if thing_tester.is_thing_error(thing_uid2):
    print(f"Thing {thing_uid2} has an error.")
else:
    print(f"Thing {thing_uid2} has no error.")

# Test if the second Thing is in PENDING state
if thing_tester.is_thing_pending(thing_uid2):
    print(f"Thing {thing_uid2} is in PENDING state.")
else:
    print(f"Thing {thing_uid2} is NOT in PENDING state.")

# Enable the second Thing
if thing_tester.enable_thing(thing_uid2):
    print(f"{thing_uid2} successfully enabled.")
else:
    print(f"Error enabling {thing_uid2}.")

# Disable the first Thing
if thing_tester.disable_thing(thing_uid):
    print(f"{thing_uid} successfully disabled.")
else:
    print(f"Error disabling {thing_uid}.")

# Test if the first Thing is ONLINE
if thing_tester.is_thing_online(thing_uid):
    print(f"Thing {thing_uid} is ONLINE.")
else:
    print(f"Thing {thing_uid} is NOT ONLINE.")

# Test if the first Thing is OFFLINE
if thing_tester.is_thing_offline(thing_uid):
    print(f"Thing {thing_uid} is OFFLINE.")
else:
    print(f"Thing {thing_uid} is NOT OFFLINE.")

# Test if the first Thing is in ERROR state
if thing_tester.is_thing_error(thing_uid):
    print(f"Thing {thing_uid} has an error.")
else:
    print(f"Thing {thing_uid} has no error.")

# Test if the first Thing is in PENDING state
if thing_tester.is_thing_pending(thing_uid):
    print(f"Thing {thing_uid} is in PENDING state.")
else:
    print(f"Thing {thing_uid} is NOT in PENDING state.")

# Test the second Thing again
if thing_tester.is_thing_online(thing_uid2):
    print(f"Thing {thing_uid2} is ONLINE.")
else:
    print(f"Thing {thing_uid2} is NOT ONLINE.")

# Test if the second Thing is OFFLINE again
if thing_tester.is_thing_offline(thing_uid2):
    print(f"Thing {thing_uid2} is OFFLINE.")
else:
    print(f"Thing {thing_uid2} is NOT OFFLINE.")

# Test if the second Thing is in ERROR state again
if thing_tester.is_thing_error(thing_uid2):
    print(f"Thing {thing_uid2} has an error.")
else:
    print(f"Thing {thing_uid2} has no error.")

# Test if the second Thing is in PENDING state again
if thing_tester.is_thing_pending(thing_uid2):
    print(f"Thing {thing_uid2} is in PENDING state.")
else:
    print(f"Thing {thing_uid2} is NOT in PENDING state.")
