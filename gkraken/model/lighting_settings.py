# This file is part of gkraken.
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
from enum import Enum
from typing import List, Optional

from gi.repository import Gdk

from gkraken.model.lighting_modes import LightingMode
from gkraken.model.lighting_speeds import LightingSpeed


class LightingChannel(Enum):
    LOGO = 'logo'
    RING = 'ring'


class LightingDirection(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'


class LightingColor:
    def __init__(self,
                 red: int = 0,
                 green: int = 0,
                 blue: int = 0
                 ):
        self.red: int = red
        self.green: int = green
        self.blue: int = blue

    @staticmethod
    def from_button_color(color: Gdk.RGBA):
        return LightingColor(int(color.red * 255), int(color.green * 255), int(color.blue * 255))

    def values(self) -> List[int]:
        return [self.red, self.green, self.blue]


class LightingColors:
    def __init__(self):
        self.colors: List[LightingColor] = []

    def add(self, color: LightingColor):
        self.colors.append(color)
        return self

    def values(self) -> List[List[int]]:
        return list(map(lambda color: color.values(), self.colors))


class LightingSettings:
    def __init__(self,
                 channel: LightingChannel,
                 mode: str,
                 colors: LightingColors,
                 speed: Optional[LightingSpeed],
                 direction: Optional[LightingDirection]):
        self.channel: LightingChannel = channel
        self.mode: str = mode
        self.colors: LightingColors = colors
        set_speed = speed.speed if speed else 'normal'
        self.speed: str = set_speed
        set_direction = direction.value if direction else 'forward'
        self.direction: str = set_direction

    @staticmethod
    def create_logo_settings(lighting_mode: LightingMode, colors: LightingColors,
                             speed: Optional[LightingSpeed] = None,
                             direction: Optional[LightingDirection] = None):
        return LightingSettings(LightingChannel.LOGO, lighting_mode.mode, colors, speed, direction)

    @staticmethod
    def create_ring_settings(lighting_mode: LightingMode, colors: LightingColors,
                             speed: Optional[LightingSpeed] = None,
                             direction: Optional[LightingDirection] = None):
        return LightingSettings(LightingChannel.RING, lighting_mode.mode, colors, speed, direction)