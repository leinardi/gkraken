# This file is part of 2kraken.
#
# Copyright (c) 2021 Roberto Leinardi and Guy Boldon
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
from typing import Dict, List


class LightingMode:
    def __init__(self,
                 mode_id: int,
                 mode: str,
                 frontend_name: str,
                 min_colors: int,
                 max_colors: int,
                 speed_enabled: bool,
                 direction_enabled: bool
                 ):
        self.mode_id: int = mode_id
        self.mode: str = mode
        self.frontend_name: str = frontend_name
        self.min_colors: int = min_colors
        self.max_colors: int = max_colors
        self.speed_enabled: bool = speed_enabled
        self.direction_enabled: bool = direction_enabled


class LightingModes:
    def __init__(self):
        self.modes_logo: Dict[int, LightingMode] = {}
        self.modes_ring: Dict[int, LightingMode] = {}

    @staticmethod
    def get_x2():
        lighting_modes = LightingModes()
        for mode in _ModesTypeX2.MODES_LOGO:
            lighting_modes.modes_logo[mode.mode_id] = mode
        for mode in _ModesTypeX2.MODES_RING:
            lighting_modes.modes_ring[mode.mode_id] = mode
        return lighting_modes

    @staticmethod
    def get_x3():
        lighting_modes = LightingModes()
        for mode in _ModesTypeX3.MODES_LOGO:
            lighting_modes.modes_logo[mode.mode_id] = mode
        for mode in _ModesTypeX3.MODES_RING:
            lighting_modes.modes_ring[mode.mode_id] = mode
        return lighting_modes

    @staticmethod
    def get_z3():
        lighting_modes = LightingModes()
        for mode in _ModesTypeZ3.MODES_LOGO:
            lighting_modes.modes_logo[mode.mode_id] = mode
        for mode in _ModesTypeZ3.MODES_RING:
            lighting_modes.modes_ring[mode.mode_id] = mode
        return lighting_modes


class _ModesTypeX2:
    MODES_LOGO: List[LightingMode] = [
        # LightingMode(),
    ]

    MODES_RING: List[LightingMode] = [
        # LightingMode(),
    ]


class _ModesTypeX3:
    # Logo modes have been adjusted to reasonable settings for the single LED, original settings left for reference
    MODES_LOGO: List[LightingMode] = [
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
        # LightingMode(10, 'covering-marquee', 'Covering Marquee', 1, 8, True, True),
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
        LightingMode(25, 'super-rainbow', 'Rainbow Individual', 0, 0, True, True),
        LightingMode(26, 'rainbow-pulse', 'Rainbow Pulse', 0, 0, True, True),
        LightingMode(27, 'loading', 'Loading', 1, 1, False, False),
        LightingMode(28, 'tai-chi', 'Tai-Chi', 1, 2, True, False),
        # LightingMode(29, 'water-cooler', 'Water Cooler', 2, 2, True, False),
        LightingMode(30, 'wings', 'Wings', 1, 1, True, False),
    ]

    MODES_RING: List[LightingMode] = [
        LightingMode(1, 'off', 'Off', 0, 0, False, False),
        LightingMode(2, 'fixed', 'Fixed', 1, 1, False, False),
        LightingMode(3, 'super-fixed', 'Fixed Individual', 1, 8, False, False),
        LightingMode(4, 'fading', 'Fade', 2, 8, True, False),
        LightingMode(5, 'spectrum-wave', 'Spectrum Wave', 0, 0, True, True),
        LightingMode(6, 'marquee-3', 'Marquee 3', 1, 1, True, True),
        LightingMode(7, 'marquee-4', 'Marquee 4', 1, 1, True, True),
        LightingMode(8, 'marquee-5', 'Marquee 5', 1, 1, True, True),
        LightingMode(9, 'marquee-6', 'Marquee 6', 1, 1, True, True),
        LightingMode(10, 'covering-marquee', 'Covering Marquee', 1, 8, True, True),
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
        LightingMode(21, 'super-breathing', 'Breathing Individual', 1, 8, True, False),
        LightingMode(22, 'candle', 'Candle', 1, 1, False, False),
        LightingMode(23, 'starry-night', 'Starry Night', 1, 1, True, False),
        LightingMode(24, 'rainbow-flow', 'Rainbow Flow', 0, 0, True, True),
        LightingMode(25, 'super-rainbow', 'Rainbow Individual', 0, 0, True, True),
        LightingMode(26, 'rainbow-pulse', 'Rainbow Pulse', 0, 0, True, True),
        LightingMode(27, 'loading', 'Loading', 1, 1, False, False),
        LightingMode(28, 'tai-chi', 'Tai-Chi', 1, 2, True, False),
        LightingMode(29, 'water-cooler', 'Water Cooler', 2, 2, True, False),
        LightingMode(30, 'wings', 'Wings', 1, 1, True, False),
    ]


class _ModesTypeZ3:
    MODES_LOGO: List[LightingMode] = [
    ]

    MODES_RING: List[LightingMode] = [
    ]
