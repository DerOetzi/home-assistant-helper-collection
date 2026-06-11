from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import DeroetziHelperEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([ExampleBinarySensor(entry)])


class ExampleBinarySensor(DeroetziHelperEntity, BinarySensorEntity):
    _attr_name = "Example Binary Sensor"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry, "example_binary_sensor")

    @property
    def is_on(self) -> bool | None:
        # TODO: return the computed binary state
        return None
