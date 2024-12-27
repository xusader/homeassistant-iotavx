import serial
from homeassistant.components.select import SelectEntity
from .const import DOMAIN

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([InputSelect(receiver)], True)

class AVReceiver:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=1)

    def send_command(self, command):
        self.ser.write(f"'{command}'".encode())  # Anführungszeichen in den Befehl einfügen

    def read_response(self):
        return self.ser.readline().decode().strip()

class InputSelect(SelectEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._input = "TV(ARC)"  # Initial input
        self._attr_options = [
            "TV(ARC)", "HDMI1", "HDMI2", "HDMI3", "HDMI4", "HDMI5",
            "HDMI6", "COAX", "OPTICAL", "ANALOG1", "ANALOG2", "BT"
        ]
        self._attr_current_option = self._input

    @property
    def name(self):
        return "AV Receiver Input"

    def select_option(self, option):
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
        if option in command_map:
            self._receiver.send_command(command_map[option])
            self._attr_current_option = option

    def update(self):
        # Update logic for input status if available
        pass

