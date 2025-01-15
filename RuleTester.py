import time
from OpenHABConnector import OpenHABConnector
import json
from openhab import CRUD

class RuleTester:
    def __init__(self, connector: OpenHABConnector):
        """
        Initializes the RuleTester with an OpenHAB connector.

        :param connector: The OpenHABConnector instance used to communicate with the OpenHAB system.
        """
        self.connector = connector

    def run_rule(self, rule_uid: str) -> bool:
        """
        Executes a rule immediately.

        :param rule_uid: The UID of the rule to be executed.
        :return: True if the rule was executed successfully, False otherwise.
        """
        if self.is_rule_disabled(rule_uid):
            print(f"Error: Rule {rule_uid} could not be executed because it is disabled.")
            return False

        endpoint = f"/rules/{rule_uid}/runnow"
        # Sending JSON data
        data = {}  # Add necessary data here if required
        response = self.connector.post(endpoint, headers={"Content-type": "application/json", "Accept": "application/json"}, data=json.dumps(data))

        print(response.text)

        if response and response.status_code == 200:
            print(f"Rule {rule_uid} executed successfully.")
            return True
        print(f"Error executing rule {rule_uid}. Response: {response}")
        return False

    def enable_rule(self, rule_uid: str) -> bool:
        """
        Enables a rule.

        :param rule_uid: The UID of the rule to be enabled.
        :return: True if the rule was successfully enabled, False otherwise.
        """
        endpoint = f"/rules/{rule_uid}/enable"
        data = "true"
        headers = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}

        # Performing the POST request
        response = self.connector.post(endpoint, headers=headers, data=data)

        if response and response.status_code == 200:
            print(f"Rule {rule_uid} enabled successfully.")
            return True
        print(f"Error enabling rule {rule_uid}. Response: {response}")
        return False

    def disable_rule(self, rule_uid: str) -> bool:
        """
        Disables a rule.

        :param rule_uid: The UID of the rule to be disabled.
        :return: True if the rule was successfully disabled, False otherwise.
        """
        endpoint = f"/rules/{rule_uid}/enable"
        data = "false"
        headers = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}

        # Performing the POST request
        response = self.connector.post(endpoint, headers=headers, data=data)

        if response and response.status_code == 200:
            print(f"Rule {rule_uid} disabled successfully.")
            return True
        print(f"Error disabling rule {rule_uid}. Response: {response}")
        return False

    def test_rule_execution(self, rule_uid: str, expected_item: str, expected_value: str) -> bool:
        """
        Tests the execution of a rule and verifies the expected outcome.

        :param rule_uid: The UID of the rule to be tested.
        :param expected_item: The item to check after rule execution.
        :param expected_value: The expected value of the item.
        :return: True if the test was successful, otherwise False.
        """
        try:
            # Run the rule
            if not self.run_rule(rule_uid):
                print(f"Error: Rule {rule_uid} could not be executed.")
                return False

            # Short pause for rule execution
            time.sleep(2)

            # Retrieve the state of the item
            crud = CRUD(self.connector.url, self.connector.username, self.connector.password)
            testItem = crud.read(expected_item)
            state = testItem.get("state")
            
            if state is None or state != expected_value:
                print(f"Error: State of item {expected_item} after rule execution does not match. Expected: {expected_value}, Found: {state}")
                return False

            print(f"{expected_item} state after rule execution: {state}")
            return state == expected_value
        except Exception as e:
            print(f"Error during rule test execution: {e}")
            return False

    def is_rule_active(self, rule_uid: str) -> bool:
        """
        Checks if the rule is active.

        :param rule_uid: The UID of the rule to check.
        :return: True if the rule is active, False otherwise.
        """
        endpoint = f"/rules/{rule_uid}"
        response = self.connector.get(endpoint, headers={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status
            status = response.get("status", {}).get("status", "UNINITIALIZED")
            print(f"Rule status: {status}")
            return status != "UNINITIALIZED"

        # Error case
        print(f"Error retrieving the status of rule {rule_uid}. Response: {response}")
        return False

    def is_rule_disabled(self, rule_uid: str) -> bool:
        """
        Checks if the rule is disabled.

        :param rule_uid: The UID of the rule to check.
        :return: True if the rule is disabled, False otherwise.
        """
        endpoint = f"/rules/{rule_uid}"
        response = self.connector.get(endpoint, headers={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status and statusDetail
            status = response.get("status", {}).get("status", "IDLE")
            status_detail = response.get("status", {}).get("statusDetail", "NONE")
            print(f"Rule status: {status}, Detail: {status_detail}")

            # Rule is disabled if status is "UNINITIALIZED" and statusDetail is "DISABLED"
            return status == "UNINITIALIZED" and status_detail == "DISABLED"

        # Error case
        print(f"Error retrieving the status of rule {rule_uid}. Response: {response}")
        return False

    def is_rule_running(self, rule_uid: str) -> bool:
        """
        Checks if the rule is currently running.

        :param rule_uid: The UID of the rule to check.
        :return: True if the rule is running, False otherwise.
        """
        endpoint = f"/rules/{rule_uid}"
        response = self.connector.get(endpoint, headers={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status
            status = response.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")

            # Rule is running if the status is "RUNNING"
            return status == "RUNNING"

        # Error case
        print(f"Error retrieving the status of rule {rule_uid}. Response: {response}")
        return False

    def is_rule_idle(self, rule_uid: str) -> bool:
        """
        Checks if the rule is in the IDLE state.

        :param rule_uid: The UID of the rule to check.
        :return: True if the rule is in the IDLE state, False otherwise.
        """
        endpoint = f"/rules/{rule_uid}"
        response = self.connector.get(endpoint, headers={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status
            status = response.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")

            # Rule is in the IDLE state if the status is "IDLE"
            return status == "IDLE"

        # Error case
        print(f"Error retrieving the status of rule {rule_uid}. Response: {response}")
        return False

    def get_rule_status(self, rule_uid: str) -> dict:
        """
        Retrieves the full status of a rule.

        :param rule_uid: The UID of the rule whose status is to be retrieved.
        :return: A dictionary containing status information or an empty dictionary in case of an error.
        """
        endpoint = f"/rules/{rule_uid}"
        response = self.connector.get(endpoint, headers={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract status information
            status_info = {
                "status": response.get("status", {}).get("status", "UNKNOWN"),
                "statusDetail": response.get("status", {}).get("statusDetail", "UNKNOWN"),
                "editable": response.get("editable", False),
                "name": response.get("name", ""),
                "uid": response.get("uid", ""),
            }
            print(f"Rule status details: {status_info}")
            return status_info

        # Error case
        print(f"Error retrieving the status of rule {rule_uid}. Response: {response}")
        return {}
