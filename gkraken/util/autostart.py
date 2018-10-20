# This file is part of gkraken.
#
# Copyright (c) 2018 Roberto Leinardi
#
# gsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gsi.  If not, see <http://www.gnu.org/licenses/>.
from pathlib import Path

from xdg.BaseDirectory import xdg_config_home

from gkraken.conf import DESKTOP_ENTRY, APP_ICON_NAME, APP_DESKTOP_ENTRY_NAME
from gkraken.util.desktop.desktop_parser import DesktopParser
from gkraken.util.path import get_data_path

AUTOSTART_FILE_PATH = Path(xdg_config_home).joinpath('autostart').joinpath(APP_DESKTOP_ENTRY_NAME)
AUTOSTART_ICON = 'Icon'
AUTOSTART_FLAG = 'X-GNOME-Autostart-enabled'


def set_autostart_enabled(is_enabled: bool) -> None:
    desktop_parser = DesktopParser(str(AUTOSTART_FILE_PATH))

    if not AUTOSTART_FILE_PATH.is_file():
        for k, v in DESKTOP_ENTRY.items():
            desktop_parser.set(k, v)
        desktop_parser.set(AUTOSTART_ICON, get_data_path(APP_ICON_NAME))

    desktop_parser.set(AUTOSTART_FLAG, str(is_enabled).lower())
    desktop_parser.write()
