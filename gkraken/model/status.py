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
from typing import Optional
from enum import Enum


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

    @staticmethod
    def get_x2(status_list: list):
        status = Status(
            status_list[_StatusTypeX2.LIQUID_TEMPERATURE.value],
            status_list[_StatusTypeX2.FAN_RPM.value],
            status_list[_StatusTypeX2.PUMP_RPM.value],
            status_list[_StatusTypeX2.FIRMWARE_VERSION.value],
        )
        return status if status.fan_rpm < 3500 else None

    @staticmethod
    def get_x3(status_list: list):
        return Status(
            status_list[_StatusTypeX3.LIQUID_TEMPERATURE.value],
            pump_rpm=status_list[_StatusTypeX3.PUMP_RPM.value],
            pump_duty=status_list[_StatusTypeX3.PUMP_DUTY.value]
        )

    @staticmethod
    def get_z3(status_list: list):
        return Status(
            status_list[_StatusTypeZ3.LIQUID_TEMPERATURE.value],
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
