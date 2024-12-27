from homeassistant.components.number import NumberEntity
from .avreceiver import AVReceiver

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([VolumeSlider(receiver)], True)

class VolumeSlider(NumberEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self._value = 0

    @property
    def name(self):
        return "Volume"

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
        vol = int(value * 10)
        self._receiver.send_command(f"@11P{vol}")
        self._value = value

    def update(self):
        """Update the state based on the receiver's reported volume."""
        self._value = self._receiver.get_status("volume")
