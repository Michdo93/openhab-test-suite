import time
import json
import re
from openhab import OpenHABClient, Items, ItemEvents


class ItemTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ItemTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.itemsAPI = Items(client)
        self.itemEventsAPI = ItemEvents(client)

    # -------------------------------------------------------------------------
    # Command validators (static helpers)
    # -------------------------------------------------------------------------

    @staticmethod
    def _isValidSwitchValue(value: str) -> bool:
        """ON or OFF."""
        return isinstance(value, str) and value.strip().upper() in ("ON", "OFF")

    @staticmethod
    def _isValidContactValue(value: str) -> bool:
        """OPEN or CLOSED (Contact only accepts postUpdate, no sendCommand)."""
        return isinstance(value, str) and value.strip().upper() in ("OPEN", "CLOSED")

    @staticmethod
    def _isValidDimmerValue(value: str) -> bool:
        """ON, OFF, INCREASE, DECREASE, or a percentage 0-100."""
        if not isinstance(value, str):
            return False
        v = value.strip().upper()
        if v in ("ON", "OFF", "INCREASE", "DECREASE"):
            return True
        try:
            num = float(v)
            return 0.0 <= num <= 100.0
        except ValueError:
            return False

    @staticmethod
    def _isValidRollershutterValue(value: str) -> bool:
        """UP, DOWN, STOP, MOVE, or a percentage 0-100."""
        if not isinstance(value, str):
            return False
        v = value.strip().upper()
        if v in ("UP", "DOWN", "STOP", "MOVE"):
            return True
        try:
            num = float(v)
            return 0.0 <= num <= 100.0
        except ValueError:
            return False

    @staticmethod
    def _isValidColorValue(value: str) -> bool:
        """
        ON, OFF, INCREASE, DECREASE, or HSB format "H,S,B"
        where H in [0,360], S in [0,100], B in [0,100].
        """
        if not isinstance(value, str):
            return False
        v = value.strip().upper()
        if v in ("ON", "OFF", "INCREASE", "DECREASE"):
            return True
        parts = value.strip().split(",")
        if len(parts) == 3:
            try:
                h, s, b = float(parts[0]), float(parts[1]), float(parts[2])
                return (0.0 <= h <= 360.0) and (0.0 <= s <= 100.0) and (0.0 <= b <= 100.0)
            except ValueError:
                return False
        return False

    @staticmethod
    def _isValidPlayerValue(value: str) -> bool:
        """PLAY, PAUSE, NEXT, PREVIOUS, REWIND, FASTFORWARD."""
        return isinstance(value, str) and value.strip().upper() in (
            "PLAY", "PAUSE", "NEXT", "PREVIOUS", "REWIND", "FASTFORWARD"
        )

    @staticmethod
    def _isValidNumberValue(value) -> bool:
        """
        Any numeric value (int or float), optionally followed by a unit,
        e.g. "20", "20.5", "20 °C", "100 %".
        """
        if value is None:
            return False
        s = str(value).strip()
        match = re.match(r'^-?\d+(\.\d+)?(\s+\S+)?$', s)
        return match is not None

    @staticmethod
    def _isValidDateTimeValue(value: str) -> bool:
        """
        ISO-8601 datetime string, e.g. "2024-01-15T08:30:00+0000"
        or "2024-01-15T08:30:00.000Z".
        """
        if not isinstance(value, str):
            return False
        pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$'
        return re.match(pattern, value.strip()) is not None

    @staticmethod
    def _isValidLocationValue(value: str) -> bool:
        """
        "lat,lon" or "lat,lon,alt" with lat in [-90,90] and lon in [-180,180].
        """
        if not isinstance(value, str):
            return False
        parts = value.strip().split(",")
        if len(parts) not in (2, 3):
            return False
        try:
            lat = float(parts[0])
            lon = float(parts[1])
            if len(parts) == 3:
                float(parts[2])
            return (-90.0 <= lat <= 90.0) and (-180.0 <= lon <= 180.0)
        except ValueError:
            return False

    @staticmethod
    def _isValidStringValue(value) -> bool:
        """Any non-None value is acceptable for a String item."""
        return value is not None

    @staticmethod
    def _isValidImageValue(value: str) -> bool:
        """
        A URL (http/https) or a Base64 data URI (data:image/...;base64,...).
        """
        if not isinstance(value, str):
            return False
        v = value.strip()
        if v.startswith("http://") or v.startswith("https://"):
            return True
        if re.match(r'^data:image/[a-zA-Z+]+;base64,', v):
            return True
        return False

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def doesItemExist(self, itemName: str) -> bool:
        """
        Checks if an item exists in the OpenHAB system.

        :param itemName: The name of the item to check.
        :return: True if the item exists, otherwise False.
        """
        raw = self.itemsAPI.getItem(itemName)
        if raw is None:
            print(f"Error: The item '{itemName}' does not exist!")
            return False
        try:
            testItem = json.loads(raw) if isinstance(raw, str) else raw
        except (json.JSONDecodeError, TypeError):
            print(f"Error: Could not parse response for item '{itemName}'.")
            return False
        if testItem and testItem.get("name") == itemName:
            return True
        print(f"Error: The item '{itemName}' does not exist!")
        return False

    def checkItemIsType(self, itemName: str, itemType: str) -> bool:
        """
        Verifies that an item is of a specific type.

        :param itemName: The name of the item to check.
        :param itemType: The expected type of the item.
        :return: True if the item is of the expected type, otherwise False.
        """
        validTypes = [
            "Color", "Contact", "DateTime", "Dimmer", "Group",
            "Image", "Location", "Number", "Player",
            "Rollershutter", "String", "Switch",
        ]
        if itemType not in validTypes:
            print(f"Error: '{itemType}' is not a valid item type.")
            return False

        try:
            raw = self.itemsAPI.getItem(itemName)
            if raw is None:
                print(f"Error: The item '{itemName}' could not be found.")
                return False
            testItem = json.loads(raw) if isinstance(raw, str) else raw
            actualType = testItem.get("type", "")
            baseType = actualType.split(":")[0]
            if baseType == itemType:
                return True
            print(
                f"Error: The item '{itemName}' is not of type '{itemType}'! "
                f"Found type: '{actualType}'"
            )
            return False
        except Exception as e:
            print(f"Error while checking item type for '{itemName}': {e}")
            return False

    def checkItemHasState(self, itemName: str, state) -> bool:
        """
        Checks if an item has a specific state.

        :param itemName: The name of the item to check.
        :param state: The expected state of the item.
        :return: True if the item has the expected state, otherwise False.
        """
        checkState = self.itemsAPI.getItemState(itemName)
        if checkState is None:
            print(f"Error: Could not retrieve the state for item '{itemName}'.")
            return False
        return checkState == str(state)

    def isGroupItem(self, itemName: str) -> bool:
        return self.checkItemIsType(itemName, "Group")

    def getGroupMembers(self, groupName: str) -> list:
        """Returns the list of member items in a group."""
        raw = self.itemsAPI.getItem(groupName, recursive=True)  # BUG FIX: was self.items
        if raw is None:
            return []
        try:
            item = json.loads(raw) if isinstance(raw, str) else raw
            return item.get("members", [])
        except (json.JSONDecodeError, TypeError):
            return []

    def doesGroupContainMember(self, groupName: str, memberName: str) -> bool:
        members = self.getGroupMembers(groupName)
        return any(m.get("name") == memberName for m in members)

    def checkGroupMemberState(self, groupName: str, memberName: str,
                               expectedState: str) -> bool:
        members = self.getGroupMembers(groupName)
        for member in members:
            if member.get("name") == memberName:
                return str(member.get("state")) == str(expectedState)
        return False

    # -------------------------------------------------------------------------
    # Per-type test methods
    # -------------------------------------------------------------------------

    def testColor(self, itemName: str, command: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Color"):
            print(f"Test failed: '{itemName}' is not of type 'Color'.")
            return False
        if not self._isValidColorValue(command):
            print(
                f"Test failed: '{command}' is not a valid Color command. "
                f"Use ON, OFF, INCREASE, DECREASE, or 'H,S,B' (e.g. '240,100,100')."
            )
            return False
        return self.__testItem(itemName, "Color", command, expectedState, timeout)

    def testContact(self, itemName: str, update: str = None, expectedState: str = None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Contact"):
            print(f"Test failed: '{itemName}' is not of type 'Contact'.")
            return False
        if update is not None and not self._isValidContactValue(update):
            print(
                f"Test failed: '{update}' is not a valid Contact update. "
                f"Use OPEN or CLOSED."
            )
            return False
        return self.__testItem(itemName, "Contact", update, expectedState, timeout)

    def testDateTime(self, itemName: str, command: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "DateTime"):
            print(f"Test failed: '{itemName}' is not of type 'DateTime'.")
            return False
        if not self._isValidDateTimeValue(command):
            print(
                f"Test failed: '{command}' is not a valid DateTime command. "
                f"Use ISO-8601 format, e.g. '2024-01-15T08:30:00+0000'."
            )
            return False
        return self.__testItem(itemName, "DateTime", command, expectedState, timeout)

    def testDimmer(self, itemName: str, command: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Dimmer"):
            print(f"Test failed: '{itemName}' is not of type 'Dimmer'.")
            return False
        if not self._isValidDimmerValue(str(command)):
            print(
                f"Test failed: '{command}' is not a valid Dimmer command. "
                f"Use ON, OFF, INCREASE, DECREASE, or a percentage value between 0 and 100."
            )
            return False
        return self.__testItem(itemName, "Dimmer", str(command), str(expectedState) if expectedState is not None else None, timeout)

    def testImage(self, itemName: str, command: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Image"):
            print(f"Test failed: '{itemName}' is not of type 'Image'.")
            return False
        if not self._isValidImageValue(command):
            print(
                f"Test failed: '{command}' is not a valid Image command. "
                f"Use an http/https URL or a Base64 data URI (data:image/...;base64,...)."
            )
            return False
        return self.__testItem(itemName, "Image", command, expectedState, timeout)

    def testLocation(self, itemName: str, update: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Location"):
            print(f"Test failed: '{itemName}' is not of type 'Location'.")
            return False
        if not self._isValidLocationValue(update):
            print(
                f"Test failed: '{update}' is not a valid Location update. "
                f"Use 'lat,lon' or 'lat,lon,alt', e.g. '48.7758,9.1829' or '48.7758,9.1829,300.0'."
            )
            return False
        return self.__testItem(itemName, "Location", update, expectedState, timeout)

    def testNumber(self, itemName: str, command, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Number"):
            print(f"Test failed: '{itemName}' is not of type 'Number'.")
            return False
        if not self._isValidNumberValue(command):
            print(
                f"Test failed: '{command}' is not a valid Number command. "
                f"Use a numeric value, optionally with a unit (e.g. '20', '20.5', '20 °C')."
            )
            return False
        return self.__testItem(
            itemName, "Number",
            str(command),
            str(expectedState) if expectedState is not None else None,
            timeout,
        )

    def testPlayer(self, itemName: str, command: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Player"):
            print(f"Test failed: '{itemName}' is not of type 'Player'.")
            return False
        if not self._isValidPlayerValue(command):
            print(
                f"Test failed: '{command}' is not a valid Player command. "
                f"Use PLAY, PAUSE, NEXT, PREVIOUS, REWIND, or FASTFORWARD."
            )
            return False
        return self.__testItem(itemName, "Player", command, expectedState, timeout)

    def testRollershutter(self, itemName: str, command: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Rollershutter"):
            print(f"Test failed: '{itemName}' is not of type 'Rollershutter'.")
            return False
        if not self._isValidRollershutterValue(command):
            print(
                f"Test failed: '{command}' is not a valid Rollershutter command. "
                f"Use UP, DOWN, STOP, MOVE, or a percentage value between 0 and 100."
            )
            return False
        return self.__testItem(itemName, "Rollershutter", command, expectedState, timeout)

    def testString(self, itemName: str, command, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "String"):
            print(f"Test failed: '{itemName}' is not of type 'String'.")
            return False
        if not self._isValidStringValue(command):
            print(f"Test failed: The command for String item '{itemName}' must not be None.")
            return False
        return self.__testItem(itemName, "String", command, expectedState, timeout)

    def testSwitch(self, itemName: str, command: str, expectedState=None, timeout: int = 10) -> bool:
        if not self.checkItemIsType(itemName, "Switch"):
            print(f"Test failed: '{itemName}' is not of type 'Switch'.")
            return False
        if not self._isValidSwitchValue(command):
            print(
                f"Test failed: '{command}' is not a valid Switch command. "
                f"Use ON or OFF."
            )
            return False
        return self.__testItem(itemName, "Switch", command, expectedState, timeout)

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def __testItem(
        self,
        itemName: str,
        itemType: str,
        commandOrUpdate=None,
        expectedState=None,
        timeout: int = 10,
    ) -> bool:
        initialState = None
        returnValue = False
        try:
            initialState = (
                self.itemsAPI.getItemState(itemName)
                if commandOrUpdate is not None
                else None
            )
            if initialState is None and commandOrUpdate is not None:
                print(f"Warning: Could not retrieve initial state for item '{itemName}'.")

            response = self.itemEventsAPI.ItemStateChangedEvent(itemName)
            if response is None:
                print(f"Error: No SSE response received for item '{itemName}'.")
                return False

            startTime = time.time()

            with response as events:
                if commandOrUpdate is not None:
                    if itemType in ("Contact", "Location"):
                        self.itemsAPI.postUpdate(itemName, str(commandOrUpdate))
                    else:
                        self.itemsAPI.sendCommand(itemName, commandOrUpdate)

                    lines = events.iter_lines()
                    while time.time() - startTime < timeout:
                        line = next(lines, None)
                        if line is None:
                            continue

                        line = line.decode()
                        if "data" not in line:
                            continue

                        try:
                            data = json.loads(line.replace("data: ", ""))
                            payload = data.get("payload")
                            eventType = data.get("type")

                            if eventType == "ItemStateChangedEvent" and payload:
                                payloadData = json.loads(payload)
                                state = payloadData.get("value")

                                if isinstance(expectedState, (list, set)):
                                    if state in expectedState:
                                        print(
                                            f"Success: '{itemName}' reached one of the "
                                            f"expected states: '{state}'"
                                        )
                                        return True
                                else:
                                    if state == expectedState:
                                        return True

                        except json.JSONDecodeError:
                            print("Warning: Event could not be converted to JSON.")

                returnValue = self.__checkFinalState(itemName, expectedState)

        except Exception as e:
            print(f"Error testing '{itemName}': {e}")
            returnValue = False

        finally:
            self.__resetItem(itemName, itemType, initialState)

        return returnValue

    def __resetItem(self, itemName: str, itemType: str, initialState) -> None:
        if initialState is not None:
            try:
                if itemType in ("Contact", "Location"):
                    self.itemsAPI.postUpdate(itemName, initialState)
                else:
                    self.itemsAPI.sendCommand(itemName, initialState)
            except Exception as e:
                print(f"Warning: Could not reset item '{itemName}' to '{initialState}': {e}")

    def __checkFinalState(self, itemName: str, expectedState) -> bool:
        if isinstance(expectedState, (list, set)):
            if not any(self.checkItemHasState(itemName, exp) for exp in expectedState):
                print(
                    f"Error: After fallback, state of '{itemName}' is not in {expectedState}."
                )
                return False
        else:
            if not self.checkItemHasState(itemName, expectedState):
                print(
                    f"Error: After fallback, state of '{itemName}' is not '{expectedState}'."
                )
                return False
        return True
