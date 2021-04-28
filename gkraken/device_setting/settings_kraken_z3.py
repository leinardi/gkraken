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

from typing import Optional, List, Dict

from liquidctl.driver.base import BaseDriver
from liquidctl.driver.kraken3 import KrakenZ3

from gkraken.device_setting.device_settings import DeviceSettings, StatusIndexType
from gkraken.model.lighting_modes import LightingMode, LightingModes
from gkraken.model.status import Status


class SettingsKrakenZ3(DeviceSettings):
    supported_driver: BaseDriver = KrakenZ3

    _status_index: Dict[StatusIndexType, int] = {
        StatusIndexType.LIQUID_TEMPERATURE: 0,
        StatusIndexType.PUMP_RPM: 1,
        StatusIndexType.PUMP_DUTY: 2,
        StatusIndexType.FAN_RPM: 3,
        StatusIndexType.FAN_DUTY: 4
    }

    # not yet supported:
    _modes_logo: List[LightingMode] = []
    _modes_ring: List[LightingMode] = []

    @classmethod
    def determine_status(cls, status_list: list) -> Optional[Status]:
        return Status(
            driver_type=cls.supported_driver,
            liquid_temperature=status_list[cls._status_index[StatusIndexType.LIQUID_TEMPERATURE]],
            fan_rpm=status_list[cls._status_index[StatusIndexType.FAN_RPM]],
            fan_duty=status_list[cls._status_index[StatusIndexType.FAN_DUTY]],
            pump_rpm=status_list[cls._status_index[StatusIndexType.PUMP_RPM]],
            pump_duty=status_list[cls._status_index[StatusIndexType.PUMP_DUTY]],
        )

    @classmethod
    def get_compatible_lighting_modes(cls) -> LightingModes:
        return LightingModes(
            modes_logo={mode.mode_id: mode for mode in cls._modes_logo},
            modes_ring={mode.mode_id: mode for mode in cls._modes_ring},
        )
