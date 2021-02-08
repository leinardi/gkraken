# This file is part of gkraken.
#
# Copyright (c) 2018 Roberto Leinardi
#
# gsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gsi.  If not, see <http://www.gnu.org/licenses/>.
import logging
import threading
from enum import Enum
from typing import Optional, List, Tuple

from injector import singleton, inject
from liquidctl.driver.usb import BaseDriver
from liquidctl.driver.kraken2 import KrakenTwoDriver
from liquidctl.driver.kraken3 import KrakenX3
from liquidctl.driver.kraken3 import KrakenZ3

from gkraken.di import INJECTOR
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
                status_list = [v for k, v, u in self._driver.get_status()]
                status = Status(
                    status_list[_StatusType.LIQUID_TEMPERATURE.value],
                    status_list[_StatusType.FAN_RPM.value],
                    status_list[_StatusType.PUMP_RPM.value],
                    status_list[_StatusType.FIRMWARE_VERSION.value]
                )
                return status if status.fan_rpm < 3500 else None
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

    def _load_driver(self) -> None:
        if not self._driver:
            self._driver = INJECTOR.get(Optional[BaseDriver])

            if self._driver:
                self._driver.connect()
            else:
                raise ValueError("Kraken USB interface error (check USB cable connection)")


class _StatusType(Enum):
    LIQUID_TEMPERATURE = 0
    FAN_RPM = 1
    PUMP_RPM = 2
    FIRMWARE_VERSION = 3
