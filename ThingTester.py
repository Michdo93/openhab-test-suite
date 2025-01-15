from OpenHABConnector import OpenHABConnector

class ThingTester:
    def __init__(self, connector: OpenHABConnector):
        """
        Initializes the ThingTester with the given OpenHAB connector.

        Parameters:
            connector (OpenHABConnector): The OpenHAB connector used to interact with the OpenHAB server.
        """
        self.connector = connector

    def _get_thing_status(self, thing_uid: str) -> str:
        """
        Retrieves the status of a Thing based on its UID.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.

        Returns:
            str: The status of the Thing (e.g., "ONLINE", "OFFLINE", etc.). Returns "UNKNOWN" if status cannot be determined.
        """
        endpoint = f"/rest/things/{thing_uid}"
        response = self.connector.get(endpoint)

        if response:
            status_info = response.get("statusInfo", {})
            return status_info.get("status", "UNKNOWN")
        return "UNKNOWN"

    def is_thing_status(self, thing_uid: str, status_to_check: str) -> bool:
        """
        Checks whether a Thing has the specified status.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.
            status_to_check (str): The status to check against (e.g., "ONLINE", "OFFLINE").

        Returns:
            bool: True if the Thing has the specified status, False otherwise.
        """
        return self._get_thing_status(thing_uid) == status_to_check

    def is_thing_online(self, thing_uid: str) -> bool:
        """
        Checks if a Thing is ONLINE.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is ONLINE, False otherwise.
        """
        return self.is_thing_status(thing_uid, "ONLINE")

    def is_thing_offline(self, thing_uid: str) -> bool:
        """
        Checks if a Thing is OFFLINE.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is OFFLINE, False otherwise.
        """
        return self.is_thing_status(thing_uid, "OFFLINE")

    def is_thing_pending(self, thing_uid: str) -> bool:
        """
        Checks if a Thing is in PENDING status.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in PENDING status, False otherwise.
        """
        return self.is_thing_status(thing_uid, "PENDING")

    def is_thing_unknown(self, thing_uid: str) -> bool:
        """
        Checks if a Thing is in UNKNOWN status.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in UNKNOWN status, False otherwise.
        """
        return self.is_thing_status(thing_uid, "UNKNOWN")

    def is_thing_uninitialized(self, thing_uid: str) -> bool:
        """
        Checks if a Thing is in UNINITIALIZED status.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in UNINITIALIZED status, False otherwise.
        """
        return self.is_thing_status(thing_uid, "UNINITIALIZED")

    def is_thing_error(self, thing_uid: str) -> bool:
        """
        Checks if a Thing is in ERROR state.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in ERROR state, False otherwise.
        """
        return self.is_thing_status(thing_uid, "ERROR")

    def enable_thing(self, thing_uid: str) -> bool:
        """
        Enables a Thing by sending a PUT request to activate it.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing to be enabled.

        Returns:
            bool: True if the Thing was successfully enabled, False otherwise.
        """
        endpoint = f"/rest/things/{thing_uid}/enable"
        data = "true"  # Enables the Thing (plain text "true")
        headers = {"Content-Type": "text/plain"}
        
        # Execute PUT request
        response = self.connector.put(endpoint, headers=headers, data=data)
        
        if response and response.status_code == 200:
            print(f"Thing {thing_uid} was successfully enabled.")
            return True
        print(f"Error enabling Thing {thing_uid}. Response: {response}")
        return False

    def disable_thing(self, thing_uid: str) -> bool:
        """
        Disables a Thing by sending a PUT request to deactivate it.

        Parameters:
            thing_uid (str): The unique identifier (UID) of the Thing to be disabled.

        Returns:
            bool: True if the Thing was successfully disabled, False otherwise.
        """
        endpoint = f"/rest/things/{thing_uid}/enable"
        data = "false"  # Disables the Thing (plain text "false")
        headers = {"Content-Type": "text/plain"}

        # Execute PUT request
        response = self.connector.put(endpoint, headers=headers, data=data)

        if response and response.status_code == 200:
            print(f"Thing {thing_uid} was successfully disabled.")
            return True
        print(f"Error disabling Thing {thing_uid}. Response: {response}")
        return False
