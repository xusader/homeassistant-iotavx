import serial
import threading
import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([IOTAVXAVX1PowerSensor(receiver), IOTAVXAVX1VolumeSensor(receiver)], True)

class AVReceiver:
    def __init__(self, port):
        """Initialize the AV Receiver."""
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)
            _LOGGER.info(f"Connected to AV Receiver on port {port}")
        except serial.SerialException as e:
            _LOGGER.error(f"Failed to connect to serial port {port}: {e}")
            raise

        self.callbacks = []
        self.running = True
        threading.Thread(target=self._read_serial, daemon=True).start()

    def _read_serial(self):
        """Continuously read from the serial port."""
        while self.running:
            try:
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode().strip()
                    _LOGGER.debug(f"Received response: {response}")
                    self._notify_callbacks(response)
            except Exception as e:
                _LOGGER.error(f"Error reading serial response: {e}")

    def send_command(self, command):
        """Send a command to the AV Receiver."""
        try:
            self.ser.write(f"'{command}'".encode())
            _LOGGER.debug(f"Sent command: '{command}'")
        except Exception as e:
            _LOGGER.error(f"Error sending command '{command}': {e}")

    def _notify_callbacks(self, response):
        """Notify all registered callbacks about a new response."""
        for callback in self.callbacks:
            callback(response)

    def register_callback(self, callback):
        """Register a callback to be notified of incoming serial data."""
        self.callbacks.append(callback)

class IOTAVXAVX1PowerSensor(Entity):
    def __init__(self, receiver):
        """Initialize the Power Sensor."""
        self._receiver = receiver
        self._state = "OFF"
        self._receiver.register_callback(self._update_callback)

    @property
    def name(self):
        return "IOTAVX AVX1 Power"

    @property
    def state(self):
        return self._state

    def _update_callback(self, response):
        """Update the power state based on the response."""
        if "DIM3*" in response:
            self._state = "ON"
        else:
            self._state = "OFF"
        self.schedule_update_ha_state()

class IOTAVXAVX1VolumeSensor(Entity):
    def __init__(self, receiver):
        """Initialize the Volume Sensor."""
        self._receiver = receiver
        self._state = 0
        self._receiver.register_callback(self._update_callback)

    @property
    def name(self):
        return "IOTAVX AVX1 Volume"

    @property
    def state(self):
        return self._state

    def _update_callback(self, response):
        """Update the volume based on the response."""
        if "@14K" in response:
            try:
                # Extract the volume from the response
                volume_str = response.split("@14K")[1]
                volume_str = ''.join(filter(str.isdigit, volume_str))  # Extract numeric part only
                self._state = int(volume_str) / 10  # Convert to a 0-80 range
                _LOGGER.debug(f"Extracted volume: {self._state}")
            except (IndexError, ValueError) as e:
                _LOGGER.error(f"Failed to parse volume from response '{response}': {e}")
        self.schedule_update_ha_state()
