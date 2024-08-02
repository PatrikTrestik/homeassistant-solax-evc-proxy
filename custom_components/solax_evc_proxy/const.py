"""Constants definition."""

from dataclasses import dataclass

DOMAIN = "solax_evc_proxy"
DEFAULT_NAME = "SolaX EVC Proxy"
ATTR_MANUFACTURER = "SolaX"

CONF_MODBUS_ADDR = "modbus_addr"

DEFAULT_SCAN_INTERVAL = 15
TIMEOUT = 10


@dataclass
class plugin_base:
    """Base for EVC Proxy plugins."""

    plugin_name: str

    def initialize(self, data) -> None:
        """Initialize."""

    async def write_data(self, address: int, payload: int) -> bool:
        """Write data."""
