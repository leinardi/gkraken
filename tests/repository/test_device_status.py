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

import pytest
from liquidctl.driver.asetek import Legacy690Lc
from liquidctl.driver.kraken2 import Kraken2
from liquidctl.driver.kraken3 import KrakenZ3, KrakenX3
from pytest_mock import MockerFixture

from gkraken.model.status import Status
from gkraken.repository.kraken_repository import KrakenRepository

TEST_DESCRIPTION: str = 'Test Device Description'


# pylint: disable=no-self-use
# pylint: disable=protected-access
class TestDeviceStatus:

    @pytest.mark.parametrize('temp, fan_rpm, pump_rpm, firmware', [
        (29.9, 853, 1948, '6.0.2'),
        (0, 0, 0, '0'),
        (88.8, 3499, 3499, '2.0.2'),
        (0, 0, None, ''),
    ])
    def test_get_status_kraken_2_success(self,
                                         repo: KrakenRepository,
                                         mocker: MockerFixture,
                                         temp: float,
                                         fan_rpm: Optional[int],
                                         pump_rpm: Optional[int],
                                         firmware: str
                                         ) -> None:
        # arrange
        driver_type = Kraken2
        mocker.patch.object(
            repo, '_driver', spec=driver_type
        )
        mocker.patch.object(
            repo._driver, 'description', TEST_DESCRIPTION
        )
        mocker.patch.object(
            repo._driver, 'get_status',
            return_value=[
                ('Liquid temperature', temp, '°C'),
                ('Fan speed', fan_rpm, 'rpm'),
                ('Pump speed', pump_rpm, 'rpm'),
                ('Firmware version', firmware, '')
            ]
        )
        # act
        status = repo.get_status()
        # assert
        assert isinstance(status, Status)
        assert status.driver_type == driver_type
        assert status.liquid_temperature == temp
        assert status.fan_rpm == fan_rpm
        assert status.fan_duty is None
        assert status.pump_rpm == pump_rpm
        assert status.pump_duty is None
        assert status.firmware_version == firmware
        assert status.device_description == TEST_DESCRIPTION

    @pytest.mark.parametrize('temp, fan_rpm, pump_rpm, firmware', [
        (88.8, 3500, 3500, '2.0.2'),
        (0, None, None, ''),
    ])
    def test_get_status_kraken_2_fail(self,
                                      repo: KrakenRepository,
                                      mocker: MockerFixture,
                                      temp: float,
                                      fan_rpm: Optional[int],
                                      pump_rpm: Optional[int],
                                      firmware: str
                                      ) -> None:
        # arrange
        driver_type = Kraken2
        mocker.patch.object(
            repo, '_driver', spec=driver_type
        )
        mocker.patch.object(
            repo._driver, 'get_status',
            return_value=[
                ('Liquid temperature', temp, '°C'),
                ('Fan speed', fan_rpm, 'rpm'),
                ('Pump speed', pump_rpm, 'rpm'),
                ('Firmware version', firmware, '')
            ]
        )
        # act & assert
        assert repo.get_status() is None

    @pytest.mark.parametrize('temp, pump_rpm, pump_duty', [
        (29.9, 1848, 90),
        (0, 0, 0),
        (88.8, 6000, 6000),
    ])
    def test_get_status_kraken_x3(self,
                                  repo: KrakenRepository,
                                  mocker: MockerFixture,
                                  temp: float,
                                  pump_rpm: Optional[int],
                                  pump_duty: Optional[int],
                                  ) -> None:
        # arrange
        driver_type = KrakenX3
        mocker.patch.object(
            repo, '_driver', spec=driver_type
        )
        mocker.patch.object(
            repo._driver, 'description', TEST_DESCRIPTION
        )
        mocker.patch.object(
            repo._driver, 'get_status',
            return_value=[
                ('Liquid temperature', temp, '°C'),
                ('Pump speed', pump_rpm, 'rpm'),
                ('Pump duty', pump_duty, '%')
            ]
        )
        # act
        status = repo.get_status()
        # assert
        assert isinstance(status, Status)
        assert status.driver_type == driver_type
        assert status.liquid_temperature == temp
        assert status.fan_rpm is None
        assert status.fan_duty is None
        assert status.pump_rpm == pump_rpm
        assert status.pump_duty == pump_duty
        assert status.firmware_version == ''
        assert status.device_description == TEST_DESCRIPTION

    @pytest.mark.parametrize('temp, pump_rpm, pump_duty, fan_rpm, fan_duty', [
        (29.9, 1848, 90, 2300, 80),
        (0, 0, 0, 0, 0),
        (88.8, 6000, 6000, 6000, 6000),
    ])
    def test_get_status_kraken_z3(self,
                                  repo: KrakenRepository,
                                  mocker: MockerFixture,
                                  temp: float,
                                  pump_rpm: Optional[int],
                                  pump_duty: Optional[int],
                                  fan_rpm: Optional[int],
                                  fan_duty: Optional[int],
                                  ) -> None:
        # arrange
        driver_type = KrakenZ3
        mocker.patch.object(
            repo, '_driver', spec=driver_type
        )
        mocker.patch.object(
            repo._driver, 'description', TEST_DESCRIPTION
        )
        mocker.patch.object(
            repo._driver, 'get_status',
            return_value=[
                ('Liquid temperature', temp, '°C'),
                ('Pump speed', pump_rpm, 'rpm'),
                ('Pump duty', pump_duty, '%'),
                ('Fan speed', fan_rpm, 'rpm'),
                ('Fan duty', fan_duty, '%'),
            ]
        )
        # act
        status = repo.get_status()
        # assert
        assert isinstance(status, Status)
        assert status.driver_type == driver_type
        assert status.liquid_temperature == temp
        assert status.fan_rpm == fan_rpm
        assert status.fan_duty == fan_duty
        assert status.pump_rpm == pump_rpm
        assert status.pump_duty == pump_duty
        assert status.firmware_version == ''
        assert status.device_description == TEST_DESCRIPTION

    @pytest.mark.parametrize('temp, fan_rpm, pump_rpm, firmware', [
        (29.9, 853, 1948, '6.0.2'),
        (0, 0, 0, '0'),
        (88.8, 3499, 3499, '2.0.2'),
        (0, 0, None, ''),
        (88.8, 3500, 3500, '2.0.2'),
        (0, None, None, ''),
    ])
    def test_get_status_kraken_legacy(self,
                                      repo: KrakenRepository,
                                      mocker: MockerFixture,
                                      temp: float,
                                      fan_rpm: Optional[int],
                                      pump_rpm: Optional[int],
                                      firmware: str
                                      ) -> None:
        # arrange
        driver_type = Legacy690Lc
        mocker.patch.object(
            repo, '_driver', spec=driver_type
        )
        mocker.patch.object(
            repo._driver, 'description', TEST_DESCRIPTION
        )
        mocker.patch.object(
            repo._driver, 'get_status',
            return_value=[
                ('Liquid temperature', temp, '°C'),
                ('Fan speed', fan_rpm, 'rpm'),
                ('Pump speed', pump_rpm, 'rpm'),
                ('Firmware version', firmware, '')
            ]
        )
        # act
        status = repo.get_status()
        # assert
        assert isinstance(status, Status)
        assert status.driver_type == driver_type
        assert status.liquid_temperature == temp
        assert status.fan_rpm == fan_rpm
        assert status.fan_duty is None
        assert status.pump_rpm == pump_rpm
        assert status.pump_duty is None
        assert status.firmware_version == firmware
        assert status.device_description == TEST_DESCRIPTION

    def test_get_status_kraken_2_no_firmware_in_status(
            self, repo: KrakenRepository, mocker: MockerFixture
    ) -> None:
        # arrange
        temp = 30
        rpm = 800
        driver_type = Kraken2
        mocker.patch.object(
            repo, '_driver', spec=driver_type
        )
        mocker.patch.object(
            repo._driver, 'description', TEST_DESCRIPTION
        )
        mocker.patch.object(
            repo._driver, 'get_status',
            return_value=[
                ('Liquid temperature', temp, '°C'),
                ('Fan speed', rpm, 'rpm'),
                ('Pump speed', rpm, 'rpm')
            ]
        )
        # act
        status = repo.get_status()
        # assert
        assert isinstance(status, Status)
        assert status.driver_type == driver_type
        assert status.liquid_temperature == temp
        assert status.fan_rpm == rpm
        assert status.fan_duty is None
        assert status.pump_rpm == rpm
        assert status.pump_duty is None
        assert status.firmware_version == ''
        assert status.device_description == TEST_DESCRIPTION

    def test_get_status_kraken_2_firmware_in_init_response(
            self, repo: KrakenRepository, mocker: MockerFixture
    ) -> None:
        # arrange
        temp = 30
        rpm = 800
        firmware = '1.2.3'
        driver_type = Kraken2
        mocker.patch.object(
            repo, '_driver', spec=driver_type
        )
        mocker.patch.object(
            repo, '_init_firmware_version', firmware
        )
        mocker.patch.object(
            repo._driver, 'description', TEST_DESCRIPTION
        )
        mocker.patch.object(
            repo._driver, 'get_status',
            return_value=[
                ('Liquid temperature', temp, '°C'),
                ('Fan speed', rpm, 'rpm'),
                ('Pump speed', rpm, 'rpm')
            ]
        )
        # act
        status = repo.get_status()
        # assert
        assert isinstance(status, Status)
        assert status.driver_type == driver_type
        assert status.liquid_temperature == temp
        assert status.fan_rpm == rpm
        assert status.fan_duty is None
        assert status.pump_rpm == rpm
        assert status.pump_duty is None
        assert status.firmware_version == firmware
        assert status.device_description == TEST_DESCRIPTION
