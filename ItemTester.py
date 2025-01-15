import time
from OpenHABConnector import OpenHABConnector
import json
from openhab import CRUD
from openhab import ItemEvent

"""
Color 	Color information (RGB) 	OnOff, IncreaseDecrease, Percent, HSB, Refresh
Contact 	Item storing status of e.g. door/window contacts 	OpenClosed, Refresh
DateTime 	Stores date and time 	DateTime
Dimmer 	Item carrying a percentage value for dimmers 	OnOff, IncreaseDecrease, Percent, Refresh
Group 	Item to nest other Items / collect them in Groups 	-
Image 	Holds the binary data of an image 	Refresh
Location 	Stores GPS coordinates 	Point, Refresh
Number 	Stores values in number format, takes an optional dimension suffix 	Decimal, Refresh
Number:<dimension> 	like Number, additional dimension information for unit support 	Quantity, Refresh
Player 	Allows to control players (e.g. audio players) 	PlayPause, NextPrevious, RewindFastforward, Refresh
Rollershutter 	Typically used for blinds 	UpDown, StopMove, Percent, Refresh
String 	Stores texts 	String, Refresh
Switch 	Typically used for lights (on/off) 	OnOff, Refresh
"""

class ItemTester:
    def __init__(self, connector: OpenHABConnector):
        """
        Initializes the ItemTester with an OpenHAB connector.

        :param connector: The OpenHABConnector instance used to communicate with the OpenHAB system.
        """
        self.connector = connector

    def does_item_exist(self, item_name):
        pass

    def check_item_is_type(self, item_name, item_type):
        pass

    def check_item_has_state(self, item_name, state):
        pass

    def test_color(self, item_name, hsb_value, valid_states):
        try:
            print(f"Teste {item_name} mit HSB-Wert {hsb_value}...")

            # Kommando senden
            crud.sendCommand(item_name, hsb_value)

            # ItemStateChangedEvent überwachen
            response = item_event.ItemStateChangedEvent(item_name)

            state = None  # Defaultwert für den Fallback
            timeout = 2  # Timeout in Sekunden
            start_time = time.time()

            with response as events:
                for line in events.iter_lines():
                    line = line.decode()

                    if "data" in line:
                        line = line.replace("data: ", "")

                        try:
                            data = json.loads(line)
                            state = data.get("state")
                            print(f"Ereignis empfangen: {state}")
                            if state in valid_states:  # Überprüfen, ob der erwartete Zustand erreicht wurde
                                break
                        except json.decoder.JSONDecodeError:
                            print("Event konnte nicht in JSON konvertiert werden")

                    # Timeout überprüfen
                    if time.time() - start_time > timeout:
                        print("Timeout erreicht, Fallback zu getState()")
                        break

            # Fallback, falls kein gültiges Ereignis empfangen wurde
            if state not in valid_states:
                state = crud.getState(item_name)
                print(f"State nach HSB-Set (Fallback): {state}")

            # Überprüfen, ob der Zustand im valid_states-Set enthalten ist
            if state in valid_states:
                print(f"Test für {item_name} bestanden.")
                return True
            else:
                print(f"Test für {item_name} nicht bestanden. Erwartet: {valid_states}, erhalten: {state}")
                return False

        except Exception as e:
            print(f"Fehler beim Testen von {item_name}: {e}")
            return False

    def test_contact(self, item_name):
        pass

    def test_datetime(self, item_name):
        pass

    def test_dimmer(self, item_name, dimmer_value):
        pass

    def test_image(self, item_name, image):
        pass

    def test_location(self, item_name, location):
        pass

    def test_number(self, item_name, number):
        pass

    def test_player(self, item_name, player_command):
        pass

    def test_rollershutter(self, item_name, command):
        pass

    def test_string(self, item_name, strings):
        try:
            state = crud.getState(item_name)
            print(f"State von {item_name}: {state}")
            return state in strings
        except Exception as e:
            print(f"Fehler beim Testen von {item_name}: {e}")
            return False

    def test_switch(self, item_name):
        try:
            print(f"Teste {item_name}...")
            # Kommando senden
            crud.sendCommand(item_name, "ON")

            # ItemStateChangedEvent überwachen
            response = item_event.ItemStateChangedEvent(item_name)

            state = None  # Defaultwert für den Fallback
            timeout = 2  # Timeout in Sekunden
            start_time = time.time()

            with response as events:
                for line in events.iter_lines():
                    line = line.decode()

                    if "data" in line:
                        line = line.replace("data: ", "")

                        try:
                            data = json.loads(line)
                            state = data.get("state")
                            print(f"Ereignis empfangen: {state}")
                            if state == "ON":  # Überprüfen, ob das Ziel erreicht ist
                                break
                        except json.decoder.JSONDecodeError:
                            print("Event konnte nicht in JSON konvertiert werden")

                    # Timeout überprüfen
                    if time.time() - start_time > timeout:
                        print("Timeout erreicht, Fallback zu getState()")
                        break

            # Fallback, falls kein gültiges Ereignis empfangen wurde
            if state != "ON":
                state = crud.getState(item_name)
                print(f"State nach ON (Fallback): {state}")

            if state != "ON":
                return False

            # Test für OFF
            crud.sendCommand(item_name, "OFF")
            start_time = time.time()
            state = None  # Zurücksetzen für OFF-Test

            with response as events:
                for line in events.iter_lines():
                    line = line.decode()

                    if "data" in line:
                        line = line.replace("data: ", "")

                        try:
                            data = json.loads(line)
                            state = data.get("state")
                            print(f"Ereignis empfangen: {state}")
                            if state == "OFF":
                                break
                        except json.decoder.JSONDecodeError:
                            print("Event konnte nicht in JSON konvertiert werden")

                    # Timeout überprüfen
                    if time.time() - start_time > timeout:
                        print("Timeout erreicht, Fallback zu getState()")
                        break

            # Fallback für OFF
            if state != "OFF":
                state = crud.getState(item_name)
                print(f"State nach OFF (Fallback): {state}")

            return state == "OFF"

        except Exception as e:
            print(f"Fehler beim Testen von {item_name}: {e}")
            return False
