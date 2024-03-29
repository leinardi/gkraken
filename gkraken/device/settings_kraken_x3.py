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
from liquidctl.driver.kraken3 import KrakenX3

from gkraken.device.device_settings import StatusIndexType, DeviceSettings
from gkraken.model.lighting_modes import LightingMode
from gkraken.model.status import Status


class SettingsKrakenX3(DeviceSettings):
    supported_driver: BaseDriver = KrakenX3

    _status_index: Dict[StatusIndexType, int] = {
        StatusIndexType.LIQUID_TEMPERATURE: 0,
        StatusIndexType.PUMP_RPM: 1,
        StatusIndexType.PUMP_DUTY: 2,
    }

    # Logo modes have been adjusted to reasonable settings for the single LED, original settings left for reference
    _modes_logo: List[LightingMode] = [
        LightingMode(1, 'off', 'Off', 0, 0, False, False),
        LightingMode(2, 'fixed', 'Fixed', 1, 1, False, False),
        # LightingMode(3, 'super-fixed', 'Fixed Individual', 1, 8, False, False),
        LightingMode(4, 'fading', 'Fade', 2, 8, True, False),
        LightingMode(5, 'spectrum-wave', 'Spectrum Wave', 0, 0, True, True),
        LightingMode(6, 'marquee-3', 'Marquee', 1, 1, True, False),
        # LightingMode(6, 'marquee-3', 'Marquee 3', 1, 1, True, True),
        # LightingMode(7, 'marquee-4', 'Marquee 4', 1, 1, True, True),
        # LightingMode(8, 'marquee-5', 'Marquee 5', 1, 1, True, True),
        # LightingMode(9, 'marquee-6', 'Marquee 6', 1, 1, True, True),
        # LightingMode(10, 'covering-marquee', 'Covering Marquee', 2, 8, True, True),
        LightingMode(11, 'alternating-3', 'Alternating', 1, 2, True, False),
        # LightingMode(11, 'alternating-3', 'Alternating 3', 1, 2, True, False),
        # LightingMode(12, 'alternating-4', 'Alternating 4', 1, 2, True, False),
        # LightingMode(13, 'alternating-5', 'Alternating 5', 1, 2, True, False),
        # LightingMode(14, 'alternating-6', 'Alternating 6', 1, 2, True, False),
        LightingMode(15, 'moving-alternating-3', 'Moving Alternating', 1, 2, True, False),
        # LightingMode(15, 'moving-alternating-3', 'Moving Alternating 3', 1, 2, True, True),
        # LightingMode(16, 'moving-alternating-4', 'Moving Alternating 4', 1, 2, True, True),
        # LightingMode(17, 'moving-alternating-5', 'Moving Alternating 5', 1, 2, True, True),
        # LightingMode(18, 'moving-alternating-6', 'Moving Alternating 6', 1, 2, True, True),
        LightingMode(19, 'pulse', 'Pulse', 1, 8, True, False),
        LightingMode(20, 'breathing', 'Breathing', 1, 8, True, False),
        # LightingMode(21, 'super-breathing', 'Breathing Individual', 1, 8, True, False),
        LightingMode(22, 'candle', 'Candle', 1, 1, False, False),
        LightingMode(23, 'starry-night', 'Starry Night', 1, 1, True, False),
        LightingMode(24, 'rainbow-flow', 'Rainbow Flow', 0, 0, True, True),
        LightingMode(25, 'super-rainbow', 'Rainbow Fade', 0, 0, True, True),
        LightingMode(26, 'rainbow-pulse', 'Rainbow Pulse', 0, 0, True, True),
        LightingMode(27, 'loading', 'Loading', 1, 1, False, False),
        LightingMode(28, 'tai-chi', 'Tai-Chi', 1, 2, True, False),
        # LightingMode(29, 'water-cooler', 'Water Cooler', 2, 2, True, False),
        LightingMode(30, 'wings', 'Wings', 1, 1, True, False),
    ]

    _modes_ring: List[LightingMode] = [
        LightingMode(1, 'off', 'Off', 0, 0, False, False),
        LightingMode(2, 'fixed', 'Fixed', 1, 1, False, False),
        LightingMode(3, 'super-fixed', 'Fixed Individual', 8, 8, False, False),
        LightingMode(4, 'fading', 'Fade', 2, 8, True, False),
        LightingMode(5, 'spectrum-wave', 'Spectrum Wave', 0, 0, True, True),
        LightingMode(6, 'marquee-3', 'Marquee 3', 1, 1, True, True),
        LightingMode(7, 'marquee-4', 'Marquee 4', 1, 1, True, True),
        LightingMode(8, 'marquee-5', 'Marquee 5', 1, 1, True, True),
        LightingMode(9, 'marquee-6', 'Marquee 6', 1, 1, True, True),
        LightingMode(10, 'covering-marquee', 'Covering Marquee', 2, 8, True, True),
        LightingMode(11, 'alternating-3', 'Alternating 3', 1, 2, True, False),
        LightingMode(12, 'alternating-4', 'Alternating 4', 1, 2, True, False),
        LightingMode(13, 'alternating-5', 'Alternating 5', 1, 2, True, False),
        LightingMode(14, 'alternating-6', 'Alternating 6', 1, 2, True, False),
        LightingMode(15, 'moving-alternating-3', 'Moving Alternating 3', 1, 2, True, True),
        LightingMode(16, 'moving-alternating-4', 'Moving Alternating 4', 1, 2, True, True),
        LightingMode(17, 'moving-alternating-5', 'Moving Alternating 5', 1, 2, True, True),
        LightingMode(18, 'moving-alternating-6', 'Moving Alternating 6', 1, 2, True, True),
        LightingMode(19, 'pulse', 'Pulse', 1, 8, True, False),
        LightingMode(20, 'breathing', 'Breathing', 1, 8, True, False),
        LightingMode(21, 'super-breathing', 'Breathing Individual', 8, 8, True, False),
        LightingMode(22, 'candle', 'Candle', 1, 1, False, False),
        LightingMode(23, 'starry-night', 'Starry Night', 1, 1, True, False),
        LightingMode(24, 'rainbow-flow', 'Rainbow Flow', 0, 0, True, True),
        LightingMode(25, 'super-rainbow', 'Rainbow Fade', 0, 0, True, True),
        LightingMode(26, 'rainbow-pulse', 'Rainbow Pulse', 0, 0, True, True),
        LightingMode(27, 'loading', 'Loading', 1, 1, False, False),
        LightingMode(28, 'tai-chi', 'Tai-Chi', 1, 2, True, False),
        LightingMode(29, 'water-cooler', 'Water Cooler', 2, 2, True, False),
        LightingMode(30, 'wings', 'Wings', 1, 1, True, False),
    ]

    @classmethod
    def determine_status(
            cls, status_list: list, device_description: str, init_firmware: Optional[str]
    ) -> Optional[Status]:
        return Status(
            driver_type=cls.supported_driver,
            firmware_version=init_firmware if init_firmware is not None else '',
            liquid_temperature=status_list[cls._status_index[StatusIndexType.LIQUID_TEMPERATURE]],
            pump_rpm=status_list[cls._status_index[StatusIndexType.PUMP_RPM]],
            pump_duty=status_list[cls._status_index[StatusIndexType.PUMP_DUTY]],
            device_description=device_description,
        )
