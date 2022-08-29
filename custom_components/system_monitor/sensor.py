import logging
import json
from click import edit
import voluptuous as vol
import datetime
import secrets
import requests
import xmltodict
import traceback
import os

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = datetime.timedelta(minutes=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.ensure_list,
    }
)


def edit_name(name):
    name = (
        name.lower()
        .replace(" ", "_")
        .replace("å", "a")
        .replace("æ", "a")
        .replace("ø", "o")
        .replace("-", "_")
        .replace(".", "")
        .replace("å", "a")
        .replace("æ", "a")
        .replace("ø", "o")
    )
    return name


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the sensor platform"""
    path = ""
    sites = {}
    devices = []

    ent_list = config.get(CONF_NAME)
    for entity in ent_list:
        friendly_name = entity["entity"]
        ip = entity["data"][0]
        port = entity["data"][1]
        name = edit_name(friendly_name)

        _LOGGER.debug("Entity from list: " + name)

        ip_http = "http://" + ip + ":" + str(port)
        ip_https = "https://" + ip + ":" + str(port)
        status = "Down"
        result = ""
        try:
            result = requests.get(ip_https)
            status = "Up"
        except requests.exceptions.SSLError as e:
            status = "Up"
        except Exception:
            pass

        if status != "Up":

            try:
                result = requests.get(ip_http)
                status = "Up"
            except requests.exceptions.SSLError as e:
                status = "Up"
            except requests.exceptions.ConnectionError as e:
                pass

        _LOGGER.debug("New sensor: " + str(name))

        devices.append(SensorDevice(name, status, friendly_name, ip_http))

        _LOGGER.info("Adding sensor: " + str(name) + " with status: " + status)

    add_devices(devices)


class SensorDevice(Entity):
    def __init__(self, name, status, friendly_name, poller):
        self._device_id = "monitor_" + name
        self._state = status
        self._friendly_name = friendly_name
        self._poller = id
        self._unique_id = name
        self._poller = poller

        # self.update()

    @Throttle(UPDATE_INTERVAL)
    def update(self):
        _LOGGER.info("Updating sensor: " + str(self._device_id))

        status = "Down"

        try:
            result = requests.get(self._poller)
            status = "Up"
        except requests.exceptions.SSLError as e:
            status = "Up"
        except requests.exceptions.ConnectionError as e:
            pass

        self._state = status

        _LOGGER.info(
            "Updated sensor: " + str(self._unique_id) + " with status: " + status
        )

    @property
    def name(self):
        """Return the name of the sensor"""
        return self._friendly_name

    @property
    def state(self):
        """Return the state of the sensor"""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor"""
        return "mdi:desktop-classic"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._unique_id
