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


"""This dynamically imports all DeviceSettings Subclasses for use at runtime."""

from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

from gkraken.device.device_settings import DeviceSettings

package_dir = Path(__file__).resolve().parent
# iterate through the modules in the current package:
for (_, module_name, _) in iter_modules([str(package_dir)]):  # type: ignore[assignment]
    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isclass(attribute) and issubclass(attribute, DeviceSettings):
            globals()[attribute_name] = attribute
