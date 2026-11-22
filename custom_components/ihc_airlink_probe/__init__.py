"""Temporary, read-only probe of IHC Airlink (RF) device diagnostics."""

import logging
import xml.etree.ElementTree as ET

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ihc_airlink_probe"
SERVICE = "airlink_dump"
IHC_DOMAIN = "ihc"
IHC_CONTROLLER = "controller"


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _read_devices(ihc_controller) -> dict:
    connection = ihc_controller.client.connection
    xdoc = connection.soap_action(
        "/ws/AirlinkManagementService", "getDetectedDeviceList", ""
    )
    if xdoc is False:
        response = getattr(connection, "last_response", None)
        return {
            "error": "no response",
            "http_status": getattr(response, "status_code", None),
            "body": getattr(response, "text", None),
            "exception": repr(getattr(connection, "last_exception", None)),
        }
    devices = [
        {_local(child.tag): child.text for child in item}
        for item in xdoc.iter()
        if _local(item.tag) == "arrayItem"
    ]
    return {"devices": devices, "raw": ET.tostring(xdoc, encoding="unicode")}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Register the dump service."""

    async def airlink_dump(_call: ServiceCall) -> dict:
        controllers = hass.data.get(IHC_DOMAIN, {})
        if not controllers:
            return {"error": "no loaded IHC controller"}
        result = {}
        for entry_id, data in controllers.items():
            result[entry_id] = await hass.async_add_executor_job(
                _read_devices, data[IHC_CONTROLLER]
            )
        _LOGGER.warning("IHC airlink dump: %s", result)
        return result

    hass.services.async_register(
        DOMAIN, SERVICE, airlink_dump, supports_response=SupportsResponse.ONLY
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Remove the service."""
    hass.services.async_remove(DOMAIN, SERVICE)
    return True
