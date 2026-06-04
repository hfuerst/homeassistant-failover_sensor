from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_state_change_event

async def async_setup_entry(hass, config_entry, async_add_entities):
    # Sensor hinzufügen und auf Options-Updates hören
    sensor = FailoverSensor(config_entry)
    async_add_entities([sensor])
    config_entry.async_on_unload(config_entry.add_to_hass(hass, sensor.update_options))

class FailoverSensor(SensorEntity):
    def __init__(self, config_entry):
        self.config_entry = config_entry
        self._attr_name = config_entry.data["name"]
        self._attr_unique_id = f"failover_{config_entry.unique_id}"
        self._active_source = None
        self.update_options()

    def update_options(self):
        """Aktualisiert die Sensoreinstellungen bei Änderungen in der UI."""
        opts = self.config_entry.options or self.config_entry.data
        self._primary = opts["primary_entity"]
        self._backups = opts["backup_entities"]
        self._entities_to_track = [self._primary] + self._backups

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_state_change_event(self.hass, self._entities_to_track, self._update_state)
        )
        self._update_state()

    def _update_state(self, event=None):
        for entity_id in self._entities_to_track:
            state_obj = self.hass.states.get(entity_id)
            if state_obj and state_obj.state not in ["unavailable", "unknown"]:
                self._attr_native_value = state_obj.state
                self._active_source = entity_id
                # Übernehme Maßeinheit automatisch
                self._attr_native_unit_of_measurement = state_obj.attributes.get("unit_of_measurement")
                self.async_write_ha_state()
                return
        
        self._attr_native_value = "unavailable"
        self._active_source = None
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self):
        """Zusatzinfos in der Entität anzeigen."""
        return {
            "active_entity": self._active_source,
            "failover_active": self._active_source != self._primary if self._active_source else False
        }
