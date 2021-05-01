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

import pytest
from pytest_mock import MockerFixture

from gkraken.repository.kraken_repository import KrakenRepository


@pytest.fixture
def repo_init() -> KrakenRepository:
    return KrakenRepository()


@pytest.fixture
def repo(repo_init: KrakenRepository, mocker: MockerFixture) -> KrakenRepository:
    # an arrange fixture for all tests
    mocker.patch.object(
        repo_init, '_load_driver'
    )
    return repo_init
