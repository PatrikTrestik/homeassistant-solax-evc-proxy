"""Plugin to connect SolaX EVC by Modbus TCP."""

import asyncio
from dataclasses import dataclass
import logging

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, Endian

from .const import plugin_base

_LOGGER = logging.getLogger(__name__)


@dataclass
class solax_evc_modbus_plugin(plugin_base):
    """Modbus TCP plugin class."""

    _lock = asyncio.Lock()
    _client: AsyncModbusTcpClient = None
    _modbus_id = 70

    def initialize(self, data):
        """Initialize plugin."""
        self._modbus_id = data["modbus_id"]
        self._client = AsyncModbusTcpClient(
            host=data["host"], port=data["port"], timeout=data["timeout"]
        )

    async def write_data(self, payload: int):
        """Write data to Modbus."""
        RefPowerToEV = 0
        PowerToEV_2 = payload
        PvRef = 0
        FeedinPower_R_2 = 0
        FeedinPower_S_2 = 0
        FeedinPower_T_2 = 0
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        builder.reset()
        builder.add_16bit_int(RefPowerToEV)
        builder.add_32bit_int(PowerToEV_2)
        builder.add_16bit_int(PvRef)
        builder.add_32bit_int(FeedinPower_R_2)
        builder.add_32bit_int(FeedinPower_S_2)
        builder.add_32bit_int(FeedinPower_T_2)
        payload = builder.to_registers()
        await self._async_write_register(0x700, payload)

    async def _async_write_register(self, address, payload: bytes):
        kwargs = {"slave": self._modbus_id}

        async with self._lock:
            if await self._check_connection():
                return await self._client.write_registers(
                    address, list(payload), **kwargs
                )

    async def _check_connection(self):
        if not self._client.connected:
            _LOGGER.info("EVC is not connected, trying to connect")
            return await self._async_connect()

        return self._client.connected

    async def _async_connect(self):
        result = False

        _LOGGER.debug(
            "Trying to connect to EVC at %s:%s",
            self._client.comm_params.host,
            self._client.comm_params.port,
        )

        result: bool
        for retry in range(2):
            result = await self._client.connect()
            if not result:
                _LOGGER.info(
                    "Connect to EVC attempt %d of 3 is not successful", retry + 1
                )
                await asyncio.sleep(1)
            else:
                break

        if result:
            _LOGGER.info(
                "EVC connected at %s:%s",
                self._client.comm_params.host,
                self._client.comm_params.port,
            )
        else:
            _LOGGER.warning(
                "Unable to connect to EVC at %s:%s",
                self._client.comm_params.host,
                self._client.comm_params.port,
            )
        return result


def get_plugin_instance():
    """Create plugin instance."""
    return solax_evc_modbus_plugin(
        plugin_name="solax_evc_modbus",
    )
