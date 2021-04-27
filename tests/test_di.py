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
from typing import Optional

from liquidctl.driver.base import BaseDriver
from liquidctl.driver.kraken2 import Kraken2
from liquidctl.driver.kraken3 import KrakenZ3, KrakenX3
from pytest_mock import MockerFixture

import gkraken.di
from gkraken.device_setting import DeviceSettings
from gkraken.device_setting.settings_kraken_2 import SettingsKraken2
from gkraken.device_setting.settings_kraken_x3 import SettingsKrakenX3
from gkraken.device_setting.settings_kraken_z3 import SettingsKrakenZ3
from gkraken.di import INJECTOR


# pylint: disable=no-self-use
class TestProvideKrakenDriver:

    def test_driver(self, mocker: MockerFixture) -> None:
        # arrange
        description = 'test device'
        mocker.patch.object(DeviceSettings, '__subclasses__', return_value=[SettingsKraken2])
        mocker.patch.object(Kraken2, 'find_supported_devices', return_value=[Kraken2('012345', description)])
        # act
        driver = INJECTOR.get(Optional[BaseDriver])
        # assert
        assert isinstance(driver, Kraken2)
        assert driver.description == description

    def test_driver_none(self, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(DeviceSettings, '__subclasses__', return_value=[SettingsKraken2])
        mocker.patch.object(Kraken2, 'find_supported_devices', return_value=[])
        # act
        driver = INJECTOR.get(Optional[BaseDriver])
        # assert
        assert driver is None

    def test_driver_multiple(self, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(DeviceSettings, '__subclasses__',
                            return_value=[SettingsKrakenZ3, SettingsKrakenX3, SettingsKraken2])
        mocker.patch.object(Kraken2, 'find_supported_devices', return_value=[Kraken2('01234', 'test device')])
        mocker.patch.object(KrakenX3, 'find_supported_devices', return_value=[KrakenX3('01234', 'test device', [], [])])
        mocker.patch.object(KrakenZ3, 'find_supported_devices',
                            return_value=[
                                KrakenZ3('01234', 'test device 1', [], []),
                                KrakenZ3('01234', 'test device 2', [], []),
                            ])
        # act
        driver = INJECTOR.get(Optional[BaseDriver])
        # assert should take the first found device from the first driver in the list of supported_drivers
        assert isinstance(driver, KrakenZ3)
        assert driver.description == 'test device 1'

    def test_driver_x_vs_z(self, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(DeviceSettings, '__subclasses__', return_value=[SettingsKrakenX3, SettingsKrakenZ3])
        mocker.patch.object(KrakenX3, 'find_supported_devices', return_value=[])
        mocker.patch.object(KrakenZ3, 'find_supported_devices',
                            return_value=[KrakenZ3('01234', 'test device z', [], []), ])
        # act
        driver = INJECTOR.get(Optional[BaseDriver])
        # assert even though the z driver is a subclass of the x driver, that it correctly pulls the right one
        assert isinstance(driver, KrakenZ3)
        assert isinstance(driver, KrakenX3)
        assert KrakenZ3 is driver.__class__
        assert KrakenX3 is not driver.__class__
