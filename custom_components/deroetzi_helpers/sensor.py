from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import DeroetziHelperEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([ExampleSensor(entry)])


class ExampleSensor(DeroetziHelperEntity, SensorEntity):
    _attr_name = "Example Sensor"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = None

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry, "example_sensor")

    @property
    def native_value(self) -> float | int | str | None:
        # TODO: return the computed sensor value
        return None
