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
from liquidctl.driver.kraken2 import Kraken2

from gkraken.conf import APP_NAME, APP_VERSION
from gkraken.model.status import Status
from gkraken.view.main_view import MainView


# pylint: disable=no-self-use
# pylint: disable=protected-access
class TestMainView:
    app_label: str = f"{APP_NAME} {APP_VERSION}"

    @pytest.mark.parametrize('status, expected_label', [
        (Status(Kraken2, 10.1, firmware_version='', device_description=''), app_label),
        (Status(Kraken2, 10.1, firmware_version='1.2.3', device_description='Device'),
         'Device  -  firmware 1.2.3  -  ' + app_label),
        (Status(Kraken2, 10.1, firmware_version='1.2.3', device_description=''),
         'firmware 1.2.3  -  ' + app_label),
        (Status(Kraken2, 10.1, firmware_version='', device_description='Device'),
         'Device  -  ' + app_label),
    ])
    def test__create_firmware_version_label(self, status: Status, expected_label: str) -> None:
        created_label = MainView._create_firmware_version_label(status)
        assert created_label == expected_label
