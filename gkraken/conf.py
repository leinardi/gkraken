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
from typing import Dict, Any

APP_PACKAGE_NAME = "gkraken"
APP_NAME = "GKraken"
APP_ID = "com.leinardi.gkraken"
APP_VERSION = "0.9.0"
APP_ICON_NAME = APP_PACKAGE_NAME + ".png"
APP_DB_NAME = APP_PACKAGE_NAME + ".db"
APP_UI_NAME = APP_PACKAGE_NAME + ".glade"
APP_SOURCE_URL = 'https://gitlab.com/leinardi/gkraken'
APP_AUTHOR = 'Roberto Leinardi'
APP_AUTHOR_EMAIL = 'roberto@leinardi.com'

FAN_MIN_DUTY = 25
FAN_MAX_DUTY = 100
PUMP_MIN_DUTY = 60
PUMP_MAX_DUTY = 100

SETTINGS_DEFAULTS: Dict[str, Any] = {
    'settings_load_last_profile': True,
    'settings_refresh_interval': 3,
    'settings_show_app_indicator': True,
    'settings_app_indicator_show_water_temp': True,
}
