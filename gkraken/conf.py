# This file is part of gkraken.
#
# Copyright (c) 2018 Roberto Leinardi
#
# gkraken is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gkraken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gkraken.  If not, see <http://www.gnu.org/licenses/>.
import os
from typing import Dict, Any

from xdg import BaseDirectory

APP_PACKAGE_NAME = "gkraken"
APP_NAME = "GKraken"
APP_ID = "com.leinardi.gkraken"
APP_VERSION = "0.7.0"
APP_ICON_NAME = APP_PACKAGE_NAME + ".png"
APP_DB_NAME = APP_PACKAGE_NAME + ".db"
APP_UI_NAME = APP_PACKAGE_NAME + ".glade"
APP_SOURCE_URL = 'https://gitlab.com/leinardi/gkraken'
APP_AUTHOR = 'Roberto Leinardi'
APP_AUTHOR_EMAIL = 'roberto@leinardi.com'

SETTINGS_DEFAULTS: Dict[str, Any] = {
    'settings_load_last_profile': False,
    'settings_show_app_indicator': True,
    'settings_app_indicator_show_water_temp': True,
}

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data_path(path: str) -> str:
    return os.path.join(_ROOT, 'data', path)


def get_config_path(file: str) -> str:
    return os.path.join(BaseDirectory.save_config_path(APP_PACKAGE_NAME), file)
