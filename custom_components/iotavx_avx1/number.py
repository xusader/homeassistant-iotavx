import serial
from homeassistant.components.number import NumberEntity
from .const import DOMAIN

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([VolumeSlider(receiver)], True)

class AVReceiver:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=1)

    def send_command(self, command):
        self.ser.write(f"{command}".encode())  # Anführungszeichen in den Befehl einfügen

    def read_response(self):
        return self.ser.readline().decode().strip()

class VolumeSlider(NumberEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._value = 40  # Initial value, this can be set to a default volume level

    @property
    def name(self):
        return "Volume Slider"

    @property
    def value(self):
        return self._value

    @property
    def min_value(self):
        return 0

    @property
    def max_value(self):
        return 80

    @property
    def step(self):
        return 0.5

    def set_value(self, value):
        self._value = value
        vol = int(value * 10)
        command = f"'@11P{vol}'"
        self._receiver.send_command(command)

