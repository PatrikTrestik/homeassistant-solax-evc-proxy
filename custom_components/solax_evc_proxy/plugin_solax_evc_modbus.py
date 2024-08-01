"""Plugin to connect SolaX EVC by Modbus TCP."""

from dataclasses import dataclass
import logging

from pymodbus.client import AsyncModbusTcpClient

from .const import plugin_base

_LOGGER = logging.getLogger(__name__)


@dataclass
class solax_evc_modbus_plugin(plugin_base):
    """Modbus TCP plugin class."""

    async def initialize(self, data):
        """Initialize plugin."""
        self._client = AsyncModbusTcpClient(
            host=data.host, port=data.port, timeout=data.timeout
        )

    async def write_data(self, address, payload):
        """Write data to Modbus."""
        await self._async_write_register(address, payload)

    async def _async_write_register(self, unit, address, payload: bytes):
        kwargs = {"slave": unit} if unit else {}

        async with self._lock:
            await self.__check_connection()
            return await self._client.write_registers(address, list(payload), **kwargs)


def get_plugin_instance():
    """Create plugin instance."""
    return solax_evc_modbus_plugin(
        plugin_name="solax_evc_modbus",
    )
