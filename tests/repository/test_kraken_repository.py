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

#  This file is part of gkraken.
#
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

from _pytest.logging import LogCaptureFixture
from liquidctl.driver.corsair_hid_psu import CorsairHidPsu
from liquidctl.driver.kraken2 import Kraken2
from liquidctl.driver.kraken3 import KrakenX3
from pytest_mock import MockerFixture

from gkraken.device import DeviceSettings
from gkraken.device.settings_kraken_2 import SettingsKraken2
from gkraken.repository.kraken_repository import KrakenRepository


# pylint: disable=no-self-use
# pylint: disable=protected-access
class TestKrakenRepository:

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

    def test_has_supported_kraken_no(self, repo_init: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(DeviceSettings, '__subclasses__', return_value=[])
        # act
        is_supported = repo_init.has_supported_kraken()
        # assert
        assert repo_init._driver is None
        assert not is_supported

    def test_has_supported_kraken_yes(self, repo_init: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(DeviceSettings, '__subclasses__', return_value=[SettingsKraken2])
        mocker.patch.object(Kraken2, 'find_supported_devices', return_value=[Kraken2('012345', 'test device')])
        mocker.patch.object(Kraken2, 'connect')
        # act
        is_supported = repo_init.has_supported_kraken()
        # assert
        assert isinstance(repo_init._driver, Kraken2)
        assert is_supported

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
