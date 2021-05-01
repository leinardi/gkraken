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

from typing import Optional

from liquidctl.driver.base import BaseDriver


class Status:
    def __init__(self,
                 driver_type: BaseDriver,
                 liquid_temperature: float,
                 firmware_version: str = '',
                 fan_rpm: int = None,
                 fan_duty: float = None,
                 pump_rpm: int = None,
                 pump_duty: int = None,
                 ) -> None:
        if not driver_type:
            raise ValueError("Status Driver Type should not be None")
        self.driver_type: BaseDriver = driver_type
        self.liquid_temperature: float = liquid_temperature
        self.firmware_version: str = firmware_version
        self.fan_rpm: Optional[int] = fan_rpm
        self.fan_duty: Optional[float] = fan_duty
        self.pump_rpm: Optional[int] = pump_rpm
        self.pump_duty: Optional[float] = pump_duty

    def __repr__(self) -> str:
        return f"{{temp: {self.liquid_temperature}, fan_rpm: {self.fan_rpm}, fan_duty: {self.fan_duty}, " \
               f"pump_rpm: {self.pump_rpm}, pump_duty: {self.pump_duty}, firmware_version: {self.firmware_version}, " \
               f"driver: {self.driver_name}}}"

    @property
    def driver_name(self) -> str:
        return str(self.driver_type.__name__)
