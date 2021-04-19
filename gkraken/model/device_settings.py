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

from enum import auto, unique, Enum
from typing import Optional, List, Dict

from liquidctl.driver.base import BaseDriver

from gkraken.model.lighting_modes import LightingMode
from gkraken.model.lighting_modes import LightingModes
from gkraken.model.status import Status


@unique
class StatusIndexType(Enum):
    LIQUID_TEMPERATURE = auto()
    FIRMWARE_VERSION = auto()
    PUMP_RPM = auto()
    PUMP_DUTY = auto()
    FAN_RPM = auto()
    FAN_DUTY = auto()


class DeviceSettings:
    SUPPORTED_DRIVER: BaseDriver = None

    _STATUS_INDEX: Dict[StatusIndexType, int] = {}

    _MODES_LOGO: List[LightingMode] = []
    _MODES_RING: List[LightingMode] = []

    def determine_status(self, status_list: list) -> Optional[Status]:
        raise NotImplementedError('This should be implemented in one of the child classes')

    def get_compatible_lighting_modes(self) -> LightingModes:
        raise NotImplementedError('This should be implemented in one of the child classes')
