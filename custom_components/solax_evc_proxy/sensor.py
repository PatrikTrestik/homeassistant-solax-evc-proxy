"""Time entities."""

import datetime
import logging

import homeassistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_MANUFACTURER, DOMAIN
from .coordinator import SolaxProxyUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    """Setups time entity."""

    name = entry.options[CONF_NAME]
    coordinator: SolaxProxyUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    device_info = {
        "identifiers": {(DOMAIN, name)},
        "name": name,
        "manufacturer": ATTR_MANUFACTURER,
    }

    entities = []
    update_time = SolaXTime(coordinator, name, device_info)

    entities.append(update_time)

    async_add_entities(entities)
    return True


class SolaXTime(CoordinatorEntity, SensorEntity):
    """Representation of an SolaX time."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, coordinator: SolaxProxyUpdateCoordinator, platform_name, device_info
    ) -> None:
        """Initialize the time."""
        super().__init__(coordinator)
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self._value: datetime.time = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data is not None:
            self._value = homeassistant.util.dt.utcnow()
            self.async_write_ha_state()

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} update time"

    @property
    def unique_id(self) -> str | None:
        return f"{self._platform_name}_update_time"

    @property
    def native_value(self) -> datetime.time:
        return self._value
