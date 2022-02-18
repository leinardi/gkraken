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
from typing import Optional, List, Dict, Tuple, Union

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
    """This is the base Device Settings class.
    To support a new device simply extend this class and override it's methods and attributes.
    It will be automatically loaded at runtime and the supported_driver will search for available devices.

    Attributes:
    ----------
    supported_driver : BaseDriver
        The supported liquidctl driver class

    _status_index : Dict[StatusIndexType, int]
        The index values for the various values reported from the liquidctl status list

    _modes_logo : List[LightingMode]
        A List of LightingMode(s) for the 'logo' channel which are supported

    _modes_ring : List[LightingMode]
        A List of LightingMode(s) for the 'ring' channel which are supported
    """

    supported_driver: BaseDriver = None

    _status_index: Dict[StatusIndexType, int] = {}

    _modes_logo: List[LightingMode] = []
    _modes_ring: List[LightingMode] = []

    @classmethod
    def determine_status(
            cls, status_list: list, device_description: str, init_firmware: Optional[str]
    ) -> Optional[Status]:
        """creates a Status object from the given liquidctl status_list"""
        raise NotImplementedError('This should be implemented in one of the child classes')

    @classmethod
    def get_compatible_lighting_modes(cls) -> LightingModes:
        """creates a LightingModes object containing the supported lighting modes for each channel.
        The default implementation works for most devices"""
        return LightingModes(
            modes_logo={mode.mode_id: mode for mode in cls._modes_logo},
            modes_ring={mode.mode_id: mode for mode in cls._modes_ring},
        )

    @classmethod
    def _safely_determine_firmware(cls, status_list: list, init_firmware: Optional[str]) -> str:
        """use the init firmware version or the version from status, depending on circumstances"""
        if init_firmware is not None:
            return init_firmware
        firmware_index = cls._status_index[StatusIndexType.FIRMWARE_VERSION]
        if len(status_list) > firmware_index:
            return str(status_list[firmware_index])
        return ''

    @staticmethod
    def find_firmware(init_status: List[Tuple]) -> Optional[str]:
        status_dict = DeviceSettings._convert_status_to_dict(init_status)
        firmware_version = status_dict.get('firmware version')
        return str(firmware_version) if firmware_version is not None else None

    @staticmethod
    def _convert_status_to_dict(lc_status: List[Tuple]) -> Dict[str, Union[str, int, float]]:
        return {
            str(lc_property).strip().lower(): value
            for lc_property, value, _ in lc_status
        }
