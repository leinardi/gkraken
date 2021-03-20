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

from typing import Dict, ValuesView, Optional


class LightingSpeed:
    def __init__(self,
                 speed_id: int,
                 speed: str,
                 frontend_name: str
                 ):
        self.speed_id: int = speed_id
        self.speed: str = speed
        self.frontend_name: str = frontend_name


class LightingSpeeds:
    def __init__(self) -> None:
        self._speeds: Dict[int, LightingSpeed] = {
            1: LightingSpeed(1, 'slowest', 'Slowest'),
            2: LightingSpeed(2, 'slower', 'Slower'),
            3: LightingSpeed(3, 'normal', 'Normal'),
            4: LightingSpeed(4, 'faster', 'Faster'),
            5: LightingSpeed(5, 'fastest', 'Fastest')
        }

    def values(self) -> ValuesView[LightingSpeed]:
        return self._speeds.values()

    def get(self, speed_id: int) -> Optional[LightingSpeed]:
        return self._speeds.get(speed_id)
