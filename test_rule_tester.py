import time
from OpenHABConnector import OpenHABConnector
from RuleTester import RuleTester

# Hier stellen wir die Verbindung zur OpenHAB API her
connector = OpenHABConnector("http://127.0.0.1:8080", "openhab", "habopen")

# Instanziierung des RuleTesters
rule_tester = RuleTester(connector)

# Beispiel: Testen der Funktionen des RuleTesters
rule_uid = "test_color-1"  # Ersetze dies mit der echten Regel-UID
expected_item = "testColor"  # Ersetze dies mit dem zu überprüfenden Item
expected_value = "240,50,50"  # Der erwartete Wert nach der Regel-Ausführung

print("Testing RuleTester...")

# Testen des Ausführens der Regel
print("\nTesting run_rule...")
run_result = rule_tester.run_rule(rule_uid)
print(f"run_rule result: {run_result}\n")

# Testen des Aktivierens der Regel
print("\nTesting enable_rule...")
enable_result = rule_tester.enable_rule(rule_uid)
print(f"enable_rule result: {enable_result}\n")

# Testen des Deaktivierens der Regel
print("\nTesting disable_rule...")
disable_result = rule_tester.disable_rule(rule_uid)
print(f"disable_rule result: {disable_result}\n")

# Testen der Regel-Ausführung und Überprüfung des Item-Zustands
print("\nTesting test_rule_execution...")
test_execution_result = rule_tester.test_rule_execution(rule_uid, expected_item, expected_value)
print(f"test_rule_execution result: {test_execution_result}\n")

# Optional: Warten, um sicherzustellen, dass alles verarbeitet wird
time.sleep(2)
print("Test completed.")
