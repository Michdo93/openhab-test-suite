import time
import json
from openhab import OpenHABClient, Rules, Items


class RuleTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the RuleTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.rulesAPI = Rules(client)
        self.__itemsAPI = Items(client)

    def _parseResponse(self, raw) -> dict:
        """Safely parse a raw API response to a dict."""
        if raw is None:
            return {}
        if isinstance(raw, dict):
            return raw
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}

    def runRule(self, ruleUID: str, contextData: dict = None) -> bool:
        """
        Executes a rule immediately.

        :param ruleUID: The UID of the rule to be executed.
        :param contextData: Optional context data for the rule execution.
        :return: True if the rule was executed successfully, False otherwise.
        """
        if self.isRuleDisabled(ruleUID):
            print(f"Error: Rule {ruleUID} could not be executed because it is disabled.")
            return False

        try:
            self.rulesAPI.runNow(ruleUID, contextData)
            print(f"Rule {ruleUID} executed successfully.")
            return True
        except Exception as e:
            print(f"Error executing rule {ruleUID}: {e}")
            return False

    def enableRule(self, ruleUID: str) -> bool:
        """
        Enables a rule.

        :param ruleUID: The UID of the rule to be enabled.
        :return: True if the rule was successfully enabled, False otherwise.
        """
        try:
            self.rulesAPI.enable(ruleUID)
            print(f"Rule {ruleUID} enabled successfully.")
            return True
        except Exception as e:
            print(f"Error enabling rule {ruleUID}: {e}")
            return False

    def disableRule(self, ruleUID: str) -> bool:
        """
        Disables a rule.

        :param ruleUID: The UID of the rule to be disabled.
        :return: True if the rule was successfully disabled, False otherwise.
        """
        try:
            self.rulesAPI.disable(ruleUID)
            print(f"Rule {ruleUID} disabled successfully.")
            return True
        except Exception as e:
            print(f"Error disabling rule {ruleUID}: {e}")
            return False

    def testRuleExecution(self, ruleUID: str, expectedItem: str, expectedValue: str) -> bool:
        """
        Tests the execution of a rule and verifies the expected outcome.

        :param ruleUID: The UID of the rule to be tested.
        :param expectedItem: The item to check after rule execution.
        :param expectedValue: The expected value of the item.
        :return: True if the test was successful, otherwise False.
        """
        try:
            if not self.runRule(ruleUID):
                print(f"Error: Rule {ruleUID} could not be executed.")
                return False

            time.sleep(2)

            state = self.__itemsAPI.getItemState(expectedItem)
            if state is None or state != expectedValue:
                print(
                    f"Error: State of item {expectedItem} after rule execution does not match. "
                    f"Expected: {expectedValue}, Found: {state}"
                )
                return False

            print(f"{expectedItem} state after rule execution: {state}")
            return state == expectedValue
        except Exception as e:
            print(f"Error during rule test execution: {e}")
            return False

    def isRuleActive(self, ruleUID: str) -> bool:
        """
        Checks if the rule is active (not UNINITIALIZED).

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is active, False otherwise.
        """
        rule = self._parseResponse(self.rulesAPI.getRule(ruleUID))
        if "status" in rule:
            status = rule.get("status", {}).get("status", "UNINITIALIZED")
            print(f"Rule status: {status}")
            return status != "UNINITIALIZED"
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def isRuleDisabled(self, ruleUID: str) -> bool:
        """
        Checks if the rule is disabled.

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is disabled, False otherwise.
        """
        rule = self._parseResponse(self.rulesAPI.getRule(ruleUID))
        if "status" in rule:
            status = rule.get("status", {}).get("status", "IDLE")
            statusDetail = rule.get("status", {}).get("statusDetail", "NONE")
            print(f"Rule status: {status}, Detail: {statusDetail}")
            return status == "UNINITIALIZED" and statusDetail == "DISABLED"
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def isRuleRunning(self, ruleUID: str) -> bool:
        """
        Checks if the rule is currently running.

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is running, False otherwise.
        """
        rule = self._parseResponse(self.rulesAPI.getRule(ruleUID))
        if "status" in rule:
            status = rule.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")
            return status == "RUNNING"
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def isRuleIdle(self, ruleUID: str) -> bool:
        """
        Checks if the rule is in the IDLE state.

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is in the IDLE state, False otherwise.
        """
        rule = self._parseResponse(self.rulesAPI.getRule(ruleUID))
        if "status" in rule:
            status = rule.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")
            return status == "IDLE"
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def getRuleStatus(self, ruleUID: str) -> dict:
        """
        Retrieves the full status of a rule.

        :param ruleUID: The UID of the rule whose status is to be retrieved.
        :return: A dictionary containing status information or an empty dictionary on error.
        """
        rule = self._parseResponse(self.rulesAPI.getRule(ruleUID))
        if "status" in rule:
            statusInfo = {
                "status": rule.get("status", {}).get("status", "UNKNOWN"),
                "statusDetail": rule.get("status", {}).get("statusDetail", "UNKNOWN"),
                "editable": rule.get("editable", False),
                "name": rule.get("name", ""),
                "uid": rule.get("uid", ""),
            }
            print(f"Rule status details: {statusInfo}")
            return statusInfo
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return {}
