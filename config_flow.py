from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
import voluptuous as vol

DOMAIN = "failover_sensor"

class FailoverConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Setze eine Unique ID basierend auf dem Namen (kleingeschrieben)
            await self.async_set_unique_id(user_input["name"].lower())
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("primary_entity"): selector.EntitySelector(),
                vol.Required("backup_entities"): selector.EntitySelector(
                    selector.EntitySelectorConfig(multiple=True)
                ),
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return FailoverOptionsFlowHandler(config_entry)

class FailoverOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Vorbelegung der Felder mit aktuellen Werten
        options = self.config_entry.options or self.config_entry.data
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("primary_entity", default=options.get("primary_entity")): selector.EntitySelector(),
                vol.Required("backup_entities", default=options.get("backup_entities")): selector.EntitySelector(
                    selector.EntitySelectorConfig(multiple=True)
                ),
            })
        )
