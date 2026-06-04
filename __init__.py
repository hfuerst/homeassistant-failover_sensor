from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "fallback_sensor"
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wird aufgerufen, wenn ein Konfigurations-Eintrag geladen wird."""
    # Registriere den Listener für nachträgliche UI-Optionen-Änderungen
    entry.async_on_unload(entry.add_to_updates_listener(async_update_options))

    # Weiterleitung an die sensor.py
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Wird aufgerufen, wenn der Nutzer die Optionen im UI ändert."""
    # Lädt die Sensor-Plattform einfach neu, um die neue Liste anzuwenden
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wird aufgerufen, wenn ein Eintrag gelöscht oder deaktiviert wird."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
