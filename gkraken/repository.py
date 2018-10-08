# This file is part of gkraken.
#
# Copyright (c) 2018 Roberto Leinardi
#
# gkraken is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gkraken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gkraken.  If not, see <http://www.gnu.org/licenses/>.

import logging
import threading
from enum import Enum
from typing import Optional, List, Tuple

from injector import singleton, inject
from liquidctl.driver.kraken_two import KrakenTwoDriver

from gkraken.model import Status
from gkraken.di import INJECTOR
from gkraken.util import synchronized_with_attr

LOG = logging.getLogger(__name__)


@singleton
class KrakenRepository:
    @inject
    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.__driver: Optional[KrakenTwoDriver] = None

    def cleanup(self) -> None:
        LOG.debug("KrakenRepository cleanup")
        if self.__driver:
            self.__driver.finalize()
            self.__driver = None

    @synchronized_with_attr("lock")
    def get_status(self) -> Optional[Status]:
        self.__load_driver()
        if self.__driver:
            try:
                status = [v for k, v, u in self.__driver.get_status()]
                return Status(
                    status[_StatusType.LIQUID_TEMPERATURE.value],
                    status[_StatusType.FAN_RPM.value],
                    status[_StatusType.PUMP_RPM.value],
                    status[_StatusType.FIRMWARE_VERSION.value]
                )
            # pylint: disable=bare-except
            except:
                LOG.exception("Error getting the status")
                self.cleanup()
        return None

    @synchronized_with_attr("lock")
    def set_speed_profile(self, channel_value: str, profile_data: List[Tuple[int, int]]) -> None:
        self.__load_driver()
        if self.__driver and profile_data:
            try:
                if len(profile_data) == 1:
                    self.__driver.set_fixed_speed(channel_value, profile_data[0][1])
                else:
                    self.__driver.set_speed_profile(channel_value, profile_data)
            # pylint: disable=bare-except
            except:
                LOG.exception("Error getting the status")
                self.cleanup()

    def __load_driver(self) -> None:
        if not self.__driver:
            self.__driver = INJECTOR.get(Optional[KrakenTwoDriver])

            if self.__driver:
                self.__driver.initialize()
            else:
                LOG.warning("KrakenTwoDriver not found!")


class _StatusType(Enum):
    LIQUID_TEMPERATURE = 0
    FAN_RPM = 1
    PUMP_RPM = 2
    FIRMWARE_VERSION = 3
