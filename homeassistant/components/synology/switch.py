"""Support for Synology Surveillance Station Cameras."""
import logging
from typing import Any

import requests
from synology.surveillance_station import SurveillanceStation

from homeassistant.components.switch import SwitchDevice

from .const import DATA_NAME, DATA_SURVEILLANCE_CLIENT, DOMAIN_DATA

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up a Synology Switches."""
    if DOMAIN_DATA in hass.data:
        data = hass.data[DOMAIN_DATA]
        if (DATA_SURVEILLANCE_CLIENT in data) and (DATA_NAME in data):
            surveillance_client = hass.data[DOMAIN_DATA][DATA_SURVEILLANCE_CLIENT]
            switches = [
                SurveillanceHomeModeSwitch(
                    surveillance_client, hass.data[DOMAIN_DATA][DATA_NAME]
                )
            ]
            async_add_entities(switches)


class SurveillanceHomeModeSwitch(SwitchDevice):
    """Synology Surveillance Station Home Mode toggle."""

    def __init__(self, surveillance_client: SurveillanceStation, name):
        """Initialize a Home Mode toggle."""
        super().__init__()
        self._surveillance_client = surveillance_client
        self._name = f"{name} Surveillance HomeMode Switch"

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return True if Home Mode is enabled."""
        try:
            return self._surveillance_client.get_home_mode_status()
        except (requests.exceptions.RequestException):
            _LOGGER.exception("Error when trying to get the status", exc_info=True)
            return False

    def turn_on(self, **kwargs: Any) -> None:
        """Enable Home Mode."""
        try:
            self._surveillance_client.set_home_mode(True)
        except (requests.exceptions.RequestException):
            _LOGGER.exception("Error when trying to enable home mode", exc_info=True)

    def turn_off(self, **kwargs: Any) -> None:
        """Disable Home Mode."""
        try:
            self._surveillance_client.set_home_mode(False)
        except (requests.exceptions.RequestException):
            _LOGGER.exception("Error when trying to disable home mode", exc_info=True)
