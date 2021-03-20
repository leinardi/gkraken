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

import os
from typing import List, Tuple


class DesktopParser(object):
    DESKTOP_SECTION = '[Desktop Entry]'

    def __init__(self, filename: str) -> None:
        self._filename = filename
        self.__property_list: List[Tuple[str, str]] = []
        self.read()
        super(DesktopParser, self).__init__()

    def read(self) -> None:
        """
        Read [Desktop Entry] section and save key=values pairs to __property_list
        """
        if os.path.exists(self._filename):
            with open(self._filename, 'r') as f:
                is_desktop_section = False
                for line in f.readlines():
                    line = line.strip(' ' + os.linesep)
                    if line == self.DESKTOP_SECTION:
                        is_desktop_section = True
                        continue
                    if line.startswith('['):
                        # another section begins
                        is_desktop_section = False
                        continue
                    if is_desktop_section and '=' in line:
                        (key, value) = line.split('=', 1)
                        self.set(key.strip(), value.strip())

    def write(self) -> None:
        """
        Write properties to the file
        """
        directory = os.path.dirname(self._filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self._filename, 'w') as f:
            f.write(os.linesep.join((self.DESKTOP_SECTION,
                                     os.linesep.join(['='.join((k, v.strip())) for k, v in self.__property_list]))))

    def get(self, name: str) -> str:
        """
        Raises KeyError if name is not found
        """

        for key, value in self.__property_list:
            if key.lower() == name.lower():
                return value
        raise KeyError('%s' % name)

    def set(self, name: str, value: str) -> None:
        if not name:
            raise ValueError("Invalid value for name: '%s'" % name)

        for i, (key, _) in enumerate(self.__property_list):
            if key.lower() == name.lower():
                self.__property_list[i] = (key, value)
                return

        self.__property_list.append((name, value))

    def get_boolean(self, name: str) -> bool:
        """
        Returns True if value is "1", "yes", "true", or "on"

        Returns False if value is "0", "no", "false", or "off"

        String values are checked in a case-insensitive manner.

        Any other value will cause it to raise ValueError.
        """

        value = self.get(name).lower()
        if value in ("1", "yes", "true", "on"):
            return True
        if value in ("0", "no", "false", "off"):
            return False

        raise ValueError("Cannot coerce '%s' to boolean" % value)
