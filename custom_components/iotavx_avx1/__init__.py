from .avreceiver import AVReceiver

DOMAIN = "iotavx_avx1"

async def async_setup(hass, config):
    """Set up the IOTAVX AVX1 integration."""
    hass.data[DOMAIN] = {}
    return True

