from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class IOTAVXAVX1ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for IOTAVX AVX1."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="IOTAVX AVX1", data=user_input)

        return self.async_show_form(step_id="user")

