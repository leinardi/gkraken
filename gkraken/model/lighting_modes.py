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

from typing import Dict


class LightingMode:
    def __init__(self,
                 mode_id: int,
                 name: str,
                 frontend_name: str,
                 min_colors: int,
                 max_colors: int,
                 speed_enabled: bool,
                 direction_enabled: bool
                 ) -> None:
        self.mode_id: int = mode_id
        self.name: str = name
        self.frontend_name: str = frontend_name
        self.min_colors: int = min_colors
        self.max_colors: int = max_colors
        self.speed_enabled: bool = speed_enabled
        self.direction_enabled: bool = direction_enabled


class LightingModes:
    def __init__(self,
                 modes_logo: Dict[int, LightingMode],
                 modes_ring: Dict[int, LightingMode],
                 ) -> None:
        self.modes_logo: Dict[int, LightingMode] = modes_logo
        self.modes_ring: Dict[int, LightingMode] = modes_ring
