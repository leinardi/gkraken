#  This file is part of gkraken.
#
#  Copyright (c) 2021 Roberto Leinardi and Guy Boldon
#
#  gkraken is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  gkraken is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with gkraken.  If not, see <http://www.gnu.org/licenses/>.

import logging
import threading
from typing import Optional, List, Tuple

from injector import singleton, inject
from liquidctl.driver.usb import BaseDriver
from liquidctl.driver.kraken2 import Kraken2, KrakenTwoDriver
from liquidctl.driver.kraken3 import KrakenX3
from liquidctl.driver.kraken3 import KrakenZ3

from gkraken.di import INJECTOR
from gkraken.model.lighting_modes import LightingModes
from gkraken.model.lighting_settings import LightingSettings
from gkraken.model.status import Status
from gkraken.util.concurrency import synchronized_with_attr

_LOG = logging.getLogger(__name__)


@singleton
class KrakenRepository:
    @inject
    def __init__(self) -> None:
        self.lock = threading.RLock()
        self._driver: Optional[BaseDriver] = None

    def has_supported_kraken(self) -> bool:
        return self._driver is not None or INJECTOR.get(Optional[BaseDriver]) is not None

    def cleanup(self) -> None:
        _LOG.debug("KrakenRepository cleanup")
        if self._driver:
            self._driver.disconnect()
            self._driver = None

    @synchronized_with_attr("lock")
    def get_status(self) -> Optional[Status]:
        self._load_driver()
        if self._driver:
            try:
                driver_status = self._driver.get_status()
                _LOG.debug("Reported status:\n%s", driver_status)
                status_list = [v for k, v, u in driver_status]
                if isinstance(self._driver, KrakenZ3):
                    return Status.get_z3(status_list)
                if isinstance(self._driver, KrakenX3):
                    return Status.get_x3(status_list)
                if isinstance(self._driver, (Kraken2, KrakenTwoDriver)):
                    return Status.get_x2(status_list)
                if self._driver:
                    _LOG.error("Driver Instance is not recognized: %s", self._driver.description)
                else:
                    _LOG.error("Race cleanup condition has removed the driver")
            # pylint: disable=bare-except
            except:
                _LOG.exception("Error getting the status")
                self.cleanup()
        return None

    @synchronized_with_attr("lock")
    def set_speed_profile(self, channel_value: str, profile_data: List[Tuple[int, int]]) -> None:
        self._load_driver()
        if self._driver and profile_data:
            try:
                if len(profile_data) == 1:
                    self._driver.set_fixed_speed(channel_value, profile_data[0][1])
                else:
                    self._driver.set_speed_profile(channel_value, profile_data)
            # pylint: disable=bare-except
            except:
                _LOG.exception("Error getting the status")
                self.cleanup()

    def get_lighting_modes(self) -> Optional[LightingModes]:
        self._load_driver()
        if isinstance(self._driver, KrakenZ3):
            return LightingModes.get_z3()
        if isinstance(self._driver, KrakenX3):
            return LightingModes.get_x3()
        if isinstance(self._driver, (Kraken2, KrakenTwoDriver)):
            return LightingModes.get_x2()
        _LOG.error("Driver Instance is not recognized: %s", self._driver.description)
        return None

    def set_lighting_mode(self, settings: LightingSettings) -> None:
        self._load_driver()
        if self._driver and settings:
            try:
                self._driver.set_color(
                    settings.channel.value,
                    settings.mode.name,
                    settings.colors.values(),
                    speed=settings.speed_or_default,
                    direction=settings.direction_or_default)
            # pylint: disable=bare-except
            except:
                _LOG.exception("Error setting the Lighting Profile")
                self.cleanup()

    def _load_driver(self) -> None:
        if not self._driver:
            self._driver = INJECTOR.get(Optional[BaseDriver])

            if self._driver:
                self._driver.connect()
            else:
                raise ValueError("Kraken USB interface error (check USB cable connection)")
