import serial
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([IOTAVXAVX1Switch(receiver)], True)
    add_entities([MuteSwitch(receiver)], True)
    add_entities([ModeSwitch(receiver)], True)
    add_entities([InputSwitch(receiver)], True)

class AVReceiver:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=1)

    def send_command(self, command):
        self.ser.write(f"'{command}'".encode())  # Anführungszeichen in den Befehl einfügen

    def read_response(self):
        return self.ser.readline().decode().strip()

    def query_mode(self):
        self.send_command("@13M")  # Annahme: '@13M' ist der Befehl zur Abfrage des Modus
        return self.read_response()

class IOTAVXAVX1Switch(SwitchEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._state = None

    @property
    def name(self):
        return "IOTAVX AVX1 Power"

    @property
    def is_on(self):
        return self._state == "ON"

    def turn_on(self, **kwargs):
        self._receiver.send_command("@112")
        self._state = "ON"

    def turn_off(self, **kwargs):
        self._receiver.send_command("@113")
        self._state = "OFF"

#    def update(self):
#        self._receiver.send_command("POWER STATUS")
#        response = self._receiver.read_response()
#        self._state = response if response in ["ON", "OFF"] else None
    def update(self):
        # Update logic for input status if available
        pass

class MuteSwitch(SwitchEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._state = False  # Initial state is not muted

    @property
    def name(self):
        return "Mute"

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._receiver.send_command("@11Q")
        self._state = True

    def turn_off(self, **kwargs):
        self._receiver.send_command("@11R")
        self._state = False

    def update(self):
        # Update logic for mute status if available
        pass

class ModeSwitch(SwitchEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._state = False  # Initial state is DIRECT

    @property
    def name(self):
        return "Mode"

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._receiver.send_command("@11E")
        self._state = True

    def turn_off(self, **kwargs):
        self._receiver.send_command("@13J")
        self._state = False

    def update(self):
        mode_status = self._receiver.query_mode()
        if mode_status == "STEREO":
            self._state = True
        elif mode_status == "DIRECT":
            self._state = False

class InputSwitch(SwitchEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._input = "TV(ARC)"  # Initial input

    @property
    def name(self):
        return "Input"

    @property
    def is_on(self):
        return self._input != "TV(ARC)"

    def turn_on(self, **kwargs):
        self.set_input("HDMI1")

    def turn_off(self, **kwargs):
        self.set_input("TV(ARC)")

    def set_input(self, input):
        command_map = {
            "TV(ARC)": "@11B",
            "HDMI1": "@116",
            "HDMI2": "@115",
            "HDMI3": "@15A",
            "HDMI4": "@15B",
            "HDMI5": "@15C",
            "HDMI6": "@15D",
            "COAX": "@117",
            "OPTICAL": "@15E",
            "ANALOG1": "@15F",
            "ANALOG2": "@15G",
            "BT": "@15H"
        }
        if input in command_map:
            self._receiver.send_command(command_map[input])
            self._input = input

    def update(self):
        # Update logic for input status if available
        pass


