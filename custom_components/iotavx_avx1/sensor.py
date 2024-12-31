import serial
from homeassistant.helpers.entity import Entity
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    port = config.get("port")
    
    # Initialize the receiver and save it to hass.data
    receiver = AVReceiver(port)
    hass.data["iotavx_avx1"] = {"receiver": receiver}

    async_add_entities([
        PowerSensor(receiver),
        VolumeSensor(receiver)
    ], True)

class AVReceiver:
    def __init__(self, port):
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)
            _LOGGER.info(f"Connected to serial port: {port}")
        except serial.SerialException as e:
            _LOGGER.error(f"Failed to connect to serial port {port}: {e}")
            raise e

    async def send_command(self, command):
        """Asynchronously send a command to the serial device."""
        try:
            self.ser.write(f"'{command}'".encode())  # Send the command with quotes
            _LOGGER.debug(f"Sent command: {command}")
        except Exception as e:
            _LOGGER.error(f"Failed to send command '{command}': {e}")

    async def read_response(self):
        """Asynchronously read response from the serial device."""
        try:
            response = self.ser.readline().decode().strip()
            _LOGGER.debug(f"Received response: {response}")
            return response
        except Exception as e:
            _LOGGER.error(f"Failed to read from serial port: {e}")
            return None

class PowerSensor(Entity):
    """Representation of the power state."""

    def __init__(self, receiver):
        self._receiver = receiver
        self._state = "OFF"

    @property
    def name(self):
        return "Power Sensor"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch the latest power state."""
        try:
            # Sending status command
            await self._receiver.send_command("@12S")
            response = await self._receiver.read_response()
            if response:
                if "DIM" in response:
                    self._state = "ON"
                else:
                    self._state = "OFF"
                _LOGGER.debug(f"Power state updated to: {self._state}")
            else:
                _LOGGER.warning("No response received for Power Sensor")
        except Exception as e:
            _LOGGER.error(f"Failed to update Power Sensor: {e}")

class VolumeSensor(Entity):
    """Representation of the volume level."""

    def __init__(self, receiver):
        self._receiver = receiver
        self._state = 0

    @property
    def name(self):
        return "Volume Sensor"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch the latest volume level."""
        try:
            # Sending volume status command
            await self._receiver.send_command("@14K")
            response = await self._receiver.read_response()
            if response:
                if "@14K" in response:
                    # Extract the volume value from the response
                    # Clean the response to remove unwanted characters
                    volume_str = response.split("@14K")[-1].strip("'")
                    try:
                        self._state = int(volume_str) / 10.0
                        _LOGGER.debug(f"Volume state updated to: {self._state}")
                    except ValueError as e:
                        _LOGGER.error(f"Error parsing volume: {e}, response: {response}")
                else:
                    _LOGGER.debug(f"Incorrect volume response: {response}")
            else:
                _LOGGER.warning("No response received for Volume Sensor")
        except Exception as e:
            _LOGGER.error(f"Failed to update Volume Sensor: {e}")
