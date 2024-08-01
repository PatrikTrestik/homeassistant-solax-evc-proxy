"""Coordinator component for EVC proxy."""

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_ID, CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_MODBUS_ADDR, DEFAULT_SCAN_INTERVAL, DOMAIN, TIMEOUT, plugin_base

_LOGGER = logging.getLogger(__name__)


class SolaxProxyUpdateCoordinator(DataUpdateCoordinator[None]):
    """Coordinator which periadicaly updates Modbus values."""

    config_entry: ConfigEntry

    def __init__(
        self, hass: HomeAssistant, config: ConfigEntry, plugin: plugin_base
    ) -> None:
        """Initialize Solax EVC Modbus updater."""

        _LOGGER.debug("Setting up coordinator")

        self._host = config.options.get(CONF_HOST, None)
        self._port = config.options.get(CONF_PORT, None)
        self._modbus_id = config.options.get(CONF_MODBUS_ADDR, None)
        self._inpuit_entity_id = config.options.get(CONF_ENTITY_ID, None)
        self.plugin = plugin
        self.plugin.initialize(
            {"host": self._host, "port": self._port, "timeout": TIMEOUT}
        )

        self.updateevent = async_track_state_change_event(
            hass, self._inpuit_entity_id, self._async_on_change
        )

        scan_interval = config.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{self._host}",
            update_interval=timedelta(seconds=scan_interval),
            request_refresh_debouncer=Debouncer(
                hass,
                _LOGGER,
                cooldown=timedelta(seconds=1),
                immediate=False,
            ),
        )

    def unload(self):
        """Cleansup environment."""

        self.updateevent()

    @callback
    def _async_on_change(self, event: Event[EventStateChangedData]) -> None:
        entity_id = event.data["entity_id"]
        old_state = event.data["old_state"]
        new_state = event.data["new_state"]

    async def _async_update_data(self):
        """Write data to SolaX EVC."""

        try:
            # This timeout is only a safeguard against the modbus methods locking
            # up. The Modbus methods themselves have their own timeouts.
            async with asyncio.timeout(10 * TIMEOUT):
                # Fetch updates
                return await self.__async_get_data()

        except SolaXProxyError as err:
            _LOGGER.exception("Writing data failed: %s", type(err).__qualname__)
            raise UpdateFailed(err) from err

    async def __async_get_data(self) -> dict:
        # Grab active context variables to limit data required to be fetched from API
        # Note: using context is not required if there is no need or ability to limit
        # data retrieved from API.
        # contexts = self.async_contexts()
        try:
            pass
        except Exception:
            _LOGGER.exception("Something went wrong reading from API")

        return {}

    async def write_register(self, address, payload):
        """Write register through plugin."""
        descr = self.plugin.write_data(address, payload)
        if descr is None:
            return False

        return False


class SolaXProxyError(Exception):
    """Base exception for all SolaX proxy errors."""
