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
from typing import Optional

import pytest
from _pytest.logging import LogCaptureFixture
from liquidctl.driver.corsair_hid_psu import CorsairHidPsu
from liquidctl.driver.kraken2 import Kraken2
from liquidctl.driver.kraken3 import KrakenX3, KrakenZ3
from pytest_mock import MockerFixture

from gkraken.model.lighting_modes import LightingModes
from gkraken.model.status import Status
from gkraken.repository.kraken_repository import KrakenRepository


# pylint: disable=no-self-use
# pylint: disable=protected-access
class TestKrakenRepository:

    @pytest.fixture(scope='function')
    def repo(self, mocker: MockerFixture) -> KrakenRepository:
        # an arrange fixture for all tests
        repo = KrakenRepository()
        mocker.patch.object(
            repo, '_load_driver'
        )
        return repo

    def test_get_none_status_when_driver_none(self, repo: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver', spec=None
        )
        # act & assert
        assert repo.get_status() is None

    def test_status_unknown_driver_type(self, repo: KrakenRepository, mocker: MockerFixture, caplog: LogCaptureFixture
                                        ) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver',
            # will likely never be supported by gkraken:
            spec=CorsairHidPsu
        )
        mocker.patch.object(
            repo._driver, 'get_status', return_value=[
                ('Fan Speed', 238, 'rpm')
            ]
        )
        caplog.at_level(logging.ERROR)
        # act
        status = repo.get_status()
        # assert
        assert status is None
        assert 'Driver Instance is not recognized' in caplog.text

    def test_driver_can_not_connect(self, repo: KrakenRepository, mocker: MockerFixture, caplog: LogCaptureFixture
                                    ) -> None:
        # arrange
        error_message = 'USB Communication Error'
        mocker.patch.object(
            repo, '_driver', spec=KrakenX3
        )
        mocker.patch.object(
            repo._driver, 'get_status', side_effect=OSError(error_message)
        )
        mocker.patch.object(repo, 'cleanup')
        caplog.at_level(logging.ERROR)
        # act
        status = repo.get_status()
        # assert
        assert status is None
        assert f'Error getting the status: {error_message}' in caplog.text
        repo.cleanup.assert_called_once()

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

    def test_get_none_lighting_when_driver_none(self, repo: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver', spec=None
        )
        # act & assert
        assert repo.get_lighting_modes() is None

    def test_lighting_unknown_driver_type(self, repo: KrakenRepository, mocker: MockerFixture, caplog: LogCaptureFixture
                                          ) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver',
            # will likely never be supported by gkraken:
            spec=CorsairHidPsu
        )
        caplog.at_level(logging.ERROR)
        # act
        lighting = repo.get_lighting_modes()
        # assert
        assert lighting is None
        assert 'Driver Instance is not recognized' in caplog.text

    def test_lighting_modes_kraken_2(self, repo: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver', spec=Kraken2
        )
        # act
        lighting_modes = repo.get_lighting_modes()
        # assert
        assert isinstance(lighting_modes, LightingModes)
        assert len(lighting_modes.modes_logo) == 6
        assert len(lighting_modes.modes_ring) == 20

    def test_lighting_modes_kraken_x3(self, repo: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver', spec=KrakenX3
        )
        # act
        lighting_modes = repo.get_lighting_modes()
        # assert
        assert isinstance(lighting_modes, LightingModes)
        assert len(lighting_modes.modes_logo) == 17
        assert len(lighting_modes.modes_ring) == 30

    def test_lighting_modes_kraken_z3(self, repo: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver', spec=KrakenZ3
        )
        # act
        lighting_modes = repo.get_lighting_modes()
        # assert
        assert isinstance(lighting_modes, LightingModes)
        assert len(lighting_modes.modes_logo) == 0
        assert len(lighting_modes.modes_ring) == 0
