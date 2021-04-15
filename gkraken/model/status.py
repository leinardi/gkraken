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
from typing import Optional, List, Tuple
from enum import Enum

from liquidctl.driver.base import BaseDriver
from liquidctl.driver.kraken2 import Kraken2
from liquidctl.driver.kraken3 import KrakenZ3, KrakenX3

_LOG = logging.getLogger(__name__)


class Status:
    def __init__(self,
                 liquid_temperature: float,
                 fan_rpm: int = None,
                 pump_rpm: int = None,
                 firmware_version: str = '',
                 pump_duty: int = None,
                 fan_duty: float = None
                 ) -> None:
        self.liquid_temperature: float = liquid_temperature
        self.fan_rpm: Optional[int] = fan_rpm
        self.fan_duty: Optional[float] = fan_duty
        self.pump_rpm: Optional[int] = pump_rpm
        self.firmware_version: str = firmware_version
        self.pump_duty: Optional[float] = pump_duty

    def __repr__(self) -> str:
        return f"{{temp: {self.liquid_temperature}, fan_rpm: {self.fan_rpm}, fan_duty: {self.fan_duty}, " \
               f"pump_rpm: {self.pump_rpm}, pump_duty: {self.pump_duty}, firmware_version: {self.firmware_version}}}"

    @staticmethod
    def get_status(driver: BaseDriver) -> 'Optional[Status]':
        driver_status = driver.get_status()
        _LOG.debug("Reported status:\n%s", driver_status)
        status_list = [v for k, v, u in driver_status]
        if isinstance(driver, KrakenZ3):
            return Status._get_z3(status_list)
        if isinstance(driver, KrakenX3):
            return Status._get_x3(status_list)
        if isinstance(driver, Kraken2):
            return Status._get_x2(status_list)
        if driver:
            _LOG.error("Driver Instance is not recognized: %s", driver.description)
        else:
            _LOG.error("Race cleanup condition has removed the driver")
        return None

    @staticmethod
    def _get_x2(status_list: list) -> 'Optional[Status]':
        status = Status(
            liquid_temperature=status_list[_StatusTypeX2.LIQUID_TEMPERATURE.value],
            fan_rpm=status_list[_StatusTypeX2.FAN_RPM.value],
            pump_rpm=status_list[_StatusTypeX2.PUMP_RPM.value],
            firmware_version=status_list[_StatusTypeX2.FIRMWARE_VERSION.value],
        )
        if status.fan_rpm is not None and status.fan_rpm < 3500:
            return status
        else:
            _LOG.error('Invalid Fan RPM from X2 Device')
            return None

    @staticmethod
    def _get_x3(status_list: list) -> 'Status':
        return Status(
            liquid_temperature=status_list[_StatusTypeX3.LIQUID_TEMPERATURE.value],
            pump_rpm=status_list[_StatusTypeX3.PUMP_RPM.value],
            pump_duty=status_list[_StatusTypeX3.PUMP_DUTY.value]
        )

    @staticmethod
    def _get_z3(status_list: list) -> 'Status':
        return Status(
            liquid_temperature=status_list[_StatusTypeZ3.LIQUID_TEMPERATURE.value],
            fan_rpm=status_list[_StatusTypeZ3.FAN_RPM.value],
            pump_rpm=status_list[_StatusTypeZ3.PUMP_RPM.value],
            pump_duty=status_list[_StatusTypeZ3.PUMP_DUTY.value],
            fan_duty=status_list[_StatusTypeZ3.FAN_DUTY.value]
        )


class _StatusTypeX2(Enum):
    LIQUID_TEMPERATURE = 0
    FAN_RPM = 1
    PUMP_RPM = 2
    FIRMWARE_VERSION = 3


class _StatusTypeX3(Enum):
    LIQUID_TEMPERATURE = 0
    PUMP_RPM = 1
    PUMP_DUTY = 2


class _StatusTypeZ3(Enum):
    LIQUID_TEMPERATURE = 0
    PUMP_RPM = 1
    PUMP_DUTY = 2
    FAN_RPM = 3
    FAN_DUTY = 4
