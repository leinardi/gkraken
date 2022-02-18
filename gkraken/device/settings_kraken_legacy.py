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
from typing import Optional, Dict, List

from liquidctl.driver.asetek import Legacy690Lc
from liquidctl.driver.base import BaseDriver

from gkraken.device.device_settings import DeviceSettings, StatusIndexType
from gkraken.model.lighting_modes import LightingMode
from gkraken.model.status import Status

_LOG = logging.getLogger(__name__)


class SettingsKrakenLegacy(DeviceSettings):
    supported_driver: BaseDriver = Legacy690Lc

    _status_index: Dict[StatusIndexType, int] = {
        StatusIndexType.LIQUID_TEMPERATURE: 0,
        StatusIndexType.FAN_RPM: 1,
        StatusIndexType.PUMP_RPM: 2,
        StatusIndexType.FIRMWARE_VERSION: 3
    }

    _modes_logo: List[LightingMode] = [
        LightingMode(1, 'blackout', 'Blackout', 0, 0, False, False),
        LightingMode(2, 'fixed', 'Fixed', 1, 1, False, False),
        LightingMode(3, 'fading', 'Fade', 2, 2, False, False),  # speed is possible, but different from other drivers
        LightingMode(4, 'blinking', 'Blinking', 1, 1, True, True),
    ]

    # no ring LEDs for this model
    _modes_ring: List[LightingMode] = []

    @classmethod
    def determine_status(
            cls, status_list: list, device_description: str, init_firmware: Optional[str]
    ) -> Optional[Status]:
        return Status(
            driver_type=cls.supported_driver,
            liquid_temperature=status_list[cls._status_index[StatusIndexType.LIQUID_TEMPERATURE]],
            firmware_version=cls._safely_determine_firmware(status_list, init_firmware),
            fan_rpm=status_list[cls._status_index[StatusIndexType.FAN_RPM]],
            pump_rpm=status_list[cls._status_index[StatusIndexType.PUMP_RPM]],
            device_description=device_description,
        )
