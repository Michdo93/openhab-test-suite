import time
from OpenHABConnector import OpenHABConnector
from RuleTester import RuleTester

# Establishing connection to the OpenHAB API
connector = OpenHABConnector("http://127.0.0.1:8080", "openhab", "habopen")

# Instantiating the RuleTester
rule_tester = RuleTester(connector)

# Example: Testing the functions of the RuleTester
rule_uid = "test_color-1"  # Replace this with the actual rule UID
expected_item = "testColor"  # Replace this with the item to be checked
expected_value = "140,50,50"  # The expected value after rule execution

print("Testing RuleTester...\n")

# Testing the retrieval of the rule status
print("Testing get_rule_status...")
status = rule_tester.get_rule_status(rule_uid)
print(f"get_rule_status result: {status}\n")

# Testing if the rule is active
print("Testing is_rule_active...")
is_active = rule_tester.is_rule_active(rule_uid)
print(f"is_rule_active result: {is_active}\n")

# Testing if the rule is disabled
print("Testing is_rule_disabled...")
is_disabled = rule_tester.is_rule_disabled(rule_uid)
print(f"is_rule_disabled result: {is_disabled}\n")

# Testing if the rule is running
print("Testing is_rule_running...")
is_running = rule_tester.is_rule_running(rule_uid)
print(f"is_rule_running result: {is_running}\n")

# Testing if the rule is in the IDLE state
print("Testing is_rule_idle...")
is_idle = rule_tester.is_rule_idle(rule_uid)
print(f"is_rule_idle result: {is_idle}\n")

# Testing enabling the rule
print("Testing enable_rule...")
enable_result = rule_tester.enable_rule(rule_uid)
print(f"enable_rule result: {enable_result}\n")

# Short wait to ensure the rule was enabled
time.sleep(1)

# Testing disabling the rule
print("Testing disable_rule...")
disable_result = rule_tester.disable_rule(rule_uid)
print(f"disable_rule result: {disable_result}\n")

# Testing rule execution
print("Testing run_rule...")
run_result = rule_tester.run_rule(rule_uid)
print(f"run_rule result: {run_result}\n")

# Testing rule execution and verifying the item state
print("Testing test_rule_execution...")
test_execution_result = rule_tester.test_rule_execution(rule_uid, expected_item, expected_value)
print(f"test_rule_execution result: {test_execution_result}\n")

# Optional: Wait to ensure everything is processed
time.sleep(2)

print("All tests completed.")
