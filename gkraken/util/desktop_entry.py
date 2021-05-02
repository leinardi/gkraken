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

from pathlib import Path

from xdg.BaseDirectory import xdg_config_home, xdg_data_home

from gkraken.conf import DESKTOP_ENTRY, APP_ICON_NAME, APP_DESKTOP_ENTRY_NAME, APP_PACKAGE_NAME
from gkraken.util.desktop.desktop_parser import DesktopParser
from gkraken.util.path import get_data_path

DESKTOP_ENTRY_EXEC = 'Exec'
DESKTOP_ENTRY_ICON = 'Icon'
AUTOSTART_FLAG = 'X-GNOME-Autostart-enabled'
AUTOSTART_FILE_PATH = Path(xdg_config_home).joinpath('autostart').joinpath(APP_DESKTOP_ENTRY_NAME)
APPLICATION_ENTRY_FILE_PATH = Path(xdg_data_home).joinpath('applications').joinpath(APP_DESKTOP_ENTRY_NAME)


def set_autostart_entry(is_enabled: bool) -> None:
    desktop_parser = DesktopParser(str(AUTOSTART_FILE_PATH))

    if not AUTOSTART_FILE_PATH.is_file():
        for key, value in DESKTOP_ENTRY.items():
            desktop_parser.set(key, value)
        desktop_parser.set(DESKTOP_ENTRY_ICON, get_data_path(APP_ICON_NAME))
        desktop_parser.set(DESKTOP_ENTRY_EXEC, '%s --hide-window' % APP_PACKAGE_NAME)

    desktop_parser.set(AUTOSTART_FLAG, str(is_enabled).lower())
    desktop_parser.write()


def add_application_entry() -> None:
    desktop_parser = DesktopParser(str(APPLICATION_ENTRY_FILE_PATH))

    for key, value in DESKTOP_ENTRY.items():
        desktop_parser.set(key, value)
    desktop_parser.set(DESKTOP_ENTRY_ICON, get_data_path(APP_ICON_NAME))
    desktop_parser.set(DESKTOP_ENTRY_EXEC, APP_PACKAGE_NAME)
    desktop_parser.write()
