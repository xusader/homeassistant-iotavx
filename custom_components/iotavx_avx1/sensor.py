import serial
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([IOTAVXAVX1Sensor(receiver)], True)

class AVReceiver:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=1)

    def send_command(self, command):
        self.ser.write(f"'{command}'".encode())  # Anführungszeichen in den Befehl einfügen

    def read_response(self):
        return self.ser.readline().decode().strip()

class IOTAVXAVX1Sensor(Entity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._state = None

    @property
    def name(self):
        return "IOTAVX AVX1"

    @property
    def state(self):
        return self._state

#    def update(self):
#        self._receiver.send_command("STATUS")
#        self._state = self._receiver.read_response()
    def update(self):
        self._receiver.send_command("@12S")
        self._state = self._receiver.read_response()


