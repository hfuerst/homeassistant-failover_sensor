from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

async def async_setup_entry(
    hass: HomeAssistant, 
    config_entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Setup der Sensor-Entität aus dem ConfigEntry."""
    
    # Auslesen aus den flexiblen .options statt aus statischen .data
    entities_list = config_entry.options.get("entities", [])
    
    unique_id = f"fallback_{config_entry.entry_id}"
    name = config_entry.title

    async_add_entities([FallbackSensor(entities_list, unique_id, name)], True)

# (Die FallbackSensor-Klasse bleibt identisch wie im vorherigen Schritt)
