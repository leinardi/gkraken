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
from liquidctl.driver.asetek import Legacy690Lc
from liquidctl.driver.kraken2 import Kraken2
from liquidctl.driver.kraken3 import KrakenX3, KrakenZ3
from pytest_mock import MockerFixture

from gkraken.model.lighting_modes import LightingModes
from gkraken.repository.kraken_repository import KrakenRepository


# pylint: disable=no-self-use
# pylint: disable=protected-access
class TestDeviceLighting:

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

    def test_lighting_modes_kraken_legacy(self, repo: KrakenRepository, mocker: MockerFixture) -> None:
        # arrange
        mocker.patch.object(
            repo, '_driver', spec=Legacy690Lc
        )
        # act
        lighting_modes = repo.get_lighting_modes()
        # assert
        assert isinstance(lighting_modes, LightingModes)
        assert len(lighting_modes.modes_logo) == 4
        assert len(lighting_modes.modes_ring) == 0
