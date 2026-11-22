"""Config flow: a single entry with no options."""

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from . import DOMAIN


class AirlinkProbeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Create the probe entry without asking anything."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="IHC Airlink Probe", data={})
