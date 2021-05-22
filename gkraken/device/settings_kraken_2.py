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

from liquidctl.driver.base import BaseDriver
from liquidctl.driver.kraken2 import Kraken2

from gkraken.device.device_settings import DeviceSettings, StatusIndexType
from gkraken.model.lighting_modes import LightingMode
from gkraken.model.status import Status

_LOG = logging.getLogger(__name__)


class SettingsKraken2(DeviceSettings):
    supported_driver: BaseDriver = Kraken2

    _status_index: Dict[StatusIndexType, int] = {
        StatusIndexType.LIQUID_TEMPERATURE: 0,
        StatusIndexType.FAN_RPM: 1,
        StatusIndexType.PUMP_RPM: 2,
        StatusIndexType.FIRMWARE_VERSION: 3
    }

    # Logo modes have been adjusted to reasonable settings for the single LED, original settings left for reference
    _modes_logo: List[LightingMode] = [
        LightingMode(1, 'off', 'Off', 0, 0, False, False),
        LightingMode(2, 'fixed', 'Fixed', 1, 1, False, False),
        # LightingMode(3, 'super-fixed', 'Fixed Individual', 1, 8, False, False),
        LightingMode(4, 'fading', 'Fade', 2, 8, True, False),
        LightingMode(5, 'spectrum-wave', 'Spectrum Wave', 0, 0, True, True),
        LightingMode(14, 'breathing', 'Breathing', 1, 8, True, False),
        # LightingMode(15, 'super-breathing', 'Breathing Individual', 1, 8, True, False),
        LightingMode(16, 'pulse', 'Pulse', 1, 8, True, False),
    ]
    _modes_ring: List[LightingMode] = [
        LightingMode(1, 'off', 'Off', 0, 0, False, False),
        LightingMode(2, 'fixed', 'Fixed', 1, 1, False, False),
        LightingMode(3, 'super-fixed', 'Fixed Individual', 8, 8, False, False),
        LightingMode(4, 'fading', 'Fade', 2, 8, True, False),
        LightingMode(5, 'spectrum-wave', 'Spectrum Wave', 0, 0, True, True),
        LightingMode(6, 'super-wave', 'Wave Individual', 8, 8, True, True),
        LightingMode(7, 'marquee-3', 'Marquee 3', 1, 1, True, True),
        LightingMode(8, 'marquee-4', 'Marquee 4', 1, 1, True, True),
        LightingMode(9, 'marquee-5', 'Marquee 5', 1, 1, True, True),
        LightingMode(10, 'marquee-6', 'Marquee 6', 1, 1, True, True),
        LightingMode(11, 'covering-marquee', 'Covering Marquee', 2, 8, True, True),
        LightingMode(12, 'alternating', 'Alternating', 2, 2, True, False),
        LightingMode(13, 'moving-alternating', 'Moving Alternating', 2, 2, True, True),
        LightingMode(14, 'breathing', 'Breathing', 1, 8, True, False),
        LightingMode(15, 'super-breathing', 'Breathing Individual', 8, 8, True, False),
        LightingMode(16, 'pulse', 'Pulse', 1, 8, True, False),
        LightingMode(17, 'tai-chi', 'Tai-Chi', 2, 2, True, False),
        LightingMode(18, 'water-cooler', 'Water Cooler', 0, 0, True, False),
        LightingMode(19, 'loading', 'Loading', 1, 1, False, False),
        LightingMode(20, 'wings', 'Wings', 1, 1, True, False),
    ]

    @classmethod
    def determine_status(cls, status_list: list, device_description: str) -> Optional[Status]:
        status = Status(
            driver_type=cls.supported_driver,
            liquid_temperature=status_list[cls._status_index[StatusIndexType.LIQUID_TEMPERATURE]],
            firmware_version=status_list[cls._status_index[StatusIndexType.FIRMWARE_VERSION]],
            fan_rpm=status_list[cls._status_index[StatusIndexType.FAN_RPM]],
            pump_rpm=status_list[cls._status_index[StatusIndexType.PUMP_RPM]],
            device_description=device_description,
        )
        if status.fan_rpm is None or status.fan_rpm >= 3500:
            _LOG.error('Invalid Fan RPM from X2 Device')
            return None
        return status
