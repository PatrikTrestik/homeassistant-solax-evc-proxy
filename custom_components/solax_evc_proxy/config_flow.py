"""Config Flow for SolaX EVC proxy component."""

from collections.abc import Mapping
import logging
import socket
from typing import Any, cast

import voluptuous as vol

from homeassistant.const import (
    CONF_ENTITY_ID,
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
)
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaCommonFlowHandler,
    SchemaConfigFlowHandler,
    SchemaFlowError,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
)
from homeassistant.helpers.selector import EntitySelector

from .const import CONF_MODBUS_ADDR, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

# ####################################################################################################

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT): str,
        vol.Required(CONF_MODBUS_ADDR): int,
        vol.Required(CONF_ENTITY_ID): EntitySelector(),
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)

OPTION_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT): str,
        vol.Required(CONF_MODBUS_ADDR): int,
        vol.Required(CONF_ENTITY_ID): EntitySelector(),
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)


async def _validate_host(handler: SchemaCommonFlowHandler, user_input: Any) -> Any:
    host = user_input[CONF_HOST]
    try:
        socket.gethostbyname(host)
    except Exception as e:
        _LOGGER.warning("Invalid host")
        raise SchemaFlowError("invalid_host") from e
    _LOGGER.info("validating host: returning data: %s", user_input)
    return user_input


CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowFormStep(CONFIG_SCHEMA, validate_user_input=_validate_host),
}
OPTIONS_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "init": SchemaFlowFormStep(OPTION_SCHEMA, validate_user_input=_validate_host),
}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow."""

    _LOGGER.info("starting configflow - domain = %s", DOMAIN)
    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Get title."""
        _LOGGER.info("title configflow %s %s:%s", DOMAIN, CONF_NAME, options)
        # Return config entry title
        return cast(str, options[CONF_NAME]) if CONF_NAME in options else ""
