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

from typing import Dict, Any

APP_PACKAGE_NAME = "gkraken"
APP_NAME = "GKraken"
APP_ID = "com.leinardi.gkraken"
APP_VERSION = "1.1.2"
APP_ICON_NAME = APP_ID
APP_ICON_NAME_SYMBOLIC = APP_ID + "-symbolic"
APP_DB_NAME = APP_PACKAGE_NAME + ".db"
APP_MAIN_UI_NAME = "main.glade"
APP_EDIT_SPEED_PROFILE_UI_NAME = "edit_speed_profile.glade"
APP_PREFERENCES_UI_NAME = "preferences.glade"
APP_DESKTOP_ENTRY_NAME = APP_PACKAGE_NAME + ".desktop"
APP_SUPPORTED_MODELS = 'NZXT Kraken X42, X52, X62, X72, X53, X63, X73, Z63 or Z73'
APP_DESCRIPTION = 'GUI to control cooling and lighting of ' + APP_SUPPORTED_MODELS + ' pumps'
APP_SOURCE_URL = 'https://gitlab.com/leinardi/gkraken'
APP_AUTHOR = 'Roberto Leinardi'
APP_AUTHOR_EMAIL = 'roberto@leinardi.com'

MIN_TEMP = 20
MAX_TEMP = 60
FAN_MIN_DUTY = 25
PUMP_MIN_DUTY = 30
MAX_DUTY = 100

SETTINGS_DEFAULTS: Dict[str, Any] = {
    'settings_launch_on_login': False,
    'settings_load_last_profile': True,
    'settings_check_new_version': False,
    'settings_minimize_to_tray': True,
    'settings_refresh_interval': 3,
    'settings_show_app_indicator': True,
    'settings_app_indicator_show_water_temp': True,
}

DESKTOP_ENTRY: Dict[str, str] = {
    'Type': 'Application',
    'Encoding': 'UTF-8',
    'Name': APP_NAME,
    'Comment': APP_DESCRIPTION,
    'Terminal': 'false',
    'Categories': 'System;Settings;',
}
