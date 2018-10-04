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
from typing import Optional

from injector import singleton, inject
from liquidctl.driver.kraken_two import KrakenTwoDriver

from gkraken.model import Status
from gkraken.di import INJECTOR

LOG = logging.getLogger(__name__)

LIQUID_TEMPERATURE = 0
FAN_RPM = 1
PUMP_RPM = 2
FIRMWARE_VERSION = 3


@singleton
class KrakenRepository:
    @inject
    def __init__(self) -> None:
        self.__driver: Optional[KrakenTwoDriver] = None
        self.__load_driver()

    def cleanup(self) -> None:
        LOG.debug("KrakenRepository cleanup")
        if self.__driver:
            self.__driver.finalize()

    def get_status(self) -> Optional[Status]:
        self.__load_driver()
        if self.__driver:
            status = [v for k, v, u in self.__driver.get_status()]
            return Status(
                status[LIQUID_TEMPERATURE],
                status[FAN_RPM],
                status[PUMP_RPM],
                status[FIRMWARE_VERSION]
            )
        return None

    def __load_driver(self) -> None:
        if not self.__driver:
            self.__driver = INJECTOR.get(Optional[KrakenTwoDriver])

            if self.__driver:
                self.__driver.initialize()
            else:
                LOG.warning("KrakenTwoDriver not found!")
