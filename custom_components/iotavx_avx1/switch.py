from homeassistant.components.switch import SwitchEntity
from .avreceiver import AVReceiver

def setup_platform(hass, config, add_entities, discovery_info=None):
    port = config.get("port")
    receiver = AVReceiver(port)
    add_entities([
        IOTAVXAVX1Switch(receiver),
        MuteSwitch(receiver)
    ], True)

class IOTAVXAVX1Switch(SwitchEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self.entity_id = "switch.iotavx_avx1_power"

    @property
    def name(self):
        return "IOTAVX AVX1 Power"

    @property
    def is_on(self):
        return self._receiver.get_status("power") == "ON"

    def turn_on(self, **kwargs):
        self._receiver.send_command("@112")

    def turn_off(self, **kwargs):
        self._receiver.send_command("@113")

class MuteSwitch(SwitchEntity):
    def __init__(self, receiver):
        self._receiver = receiver
        self.entity_id = "switch.iotavx_avx1_mute"

    @property
    def name(self):
        return "IOTAVX AVX1 Mute"

    @property
    def is_on(self):
        return self._receiver.get_status("mute")

    def turn_on(self, **kwargs):
        self._receiver.send_command("@11Q")
        self._receiver.current_status["mute"] = True

    def turn_off(self, **kwargs):
        self._receiver.send_command("@11R")
        self._receiver.current_status["mute"] = False

