"""SolaX EVC proxy integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant

from . import plugin_solax_evc_modbus
from .const import DOMAIN
from .coordinator import SolaxProxyUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def config_entry_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup(hass, config):
    """Set up the SolaX EVC proxy component."""
    hass.data[DOMAIN] = {}
    _LOGGER.debug("solax data %s", hass.data[DOMAIN])
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a SolaX EVC proxy."""
    _LOGGER.debug("setup entries - data: %s, options: %s", entry.data, entry.options)
    config = entry.options
    name = config[CONF_NAME]

    _LOGGER.debug("Setup %s.%s", DOMAIN, name)

    plugin = plugin_solax_evc_modbus.get_plugin_instance()
    coordinator = SolaxProxyUpdateCoordinator(hass, entry, plugin)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(config_entry_update_listener))
    return True


async def async_unload_entry(hass, entry):
    """Unload SolaX EVC proxy entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    ok = coordinator.unload()
    for component in PLATFORMS:
        ok = ok and await hass.config_entries.async_forward_entry_unload(
            entry, component
        )
    if not ok:
        return False

    return True
