import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

DOMAIN = "fallback_sensor"

class FallbackSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Verwaltet den initialen Setup-Ablauf (UI) für die Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Erster Schritt beim Hinzufügen der Integration."""
        if user_input is not None:
            title = user_input["name"]
            unique_id = f"fallback_helper_{title.lower().replace(' ', '_')}"
            
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            # Wichtig: Daten fließen in 'options', damit sie editierbar sind
            return self.async_create_entry(
                title=title,
                data={},
                options={"entities": user_input["entities"]}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("entities"): EntitySelector(
                    EntitySelectorConfig(multiple=True)
                ),
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Verknüpft den OptionsFlow mit dem ConfigFlow."""
        return FallbackSensorOptionsFlowHandler(config_entry)


class FallbackSensorOptionsFlowHandler(config_entries.OptionsFlow):
    """Verwaltet Änderungen über die 'Optionen'-Schaltfläche."""

    def __init__(self, config_entry):
        """Initialisiere den Options-Handler."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Zeigt den Dialog zum Bearbeiten der Entitäten-Reihenfolge."""
        if user_input is not None:
            # Aktualisiert die Optionen mit der neuen Auswahl/Reihenfolge
            return self.async_create_entry(title="", data=user_input)

        # Holt die aktuell gespeicherte Liste als Standardwert
        current_entities = self.config_entry.options.get("entities", [])

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "entities", 
                    default=current_entities
                ): EntitySelector(
                    EntitySelectorConfig(multiple=True)
                ),
            })
        )
