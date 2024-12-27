import serial
from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([VolumeUpButton(receiver)], True)
    add_entities([VolumeDownButton(receiver)], True)

class AVReceiver:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=1)

    def send_command(self, command):
        self.ser.write(f"'{command}'".encode())  # Anführungszeichen in den Befehl einfügen

    def read_response(self):
        return self.ser.readline().decode().strip()

class VolumeUpButton(ButtonEntity):
    def __init__(self, receiver):
        self._receiver = receiver

    @property
    def name(self):
        return "Volume Up"

    def press(self):
        self._receiver.send_command("@11S")

class VolumeDownButton(ButtonEntity):
    def __init__(self, receiver):
        self._receiver = receiver

    @property
    def name(self):
        return "Volume Down"

    def press(self):
        self._receiver.send_command("@11T")

