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


import logging
import os
import shutil
import subprocess
from pathlib import Path

from xdg import BaseDirectory

from gkraken.conf import APP_PACKAGE_NAME

LOG = logging.getLogger(__name__)
UDEV_RULES_DIR = '/lib/udev/rules.d/'
UDEV_RULE_FILE_NAME = '60-gkraken.rules'


def synchronized_with_attr(lock_name):
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator


LOG_DEBUG_FORMAT = '%(filename)15s:%(lineno)-4d %(asctime)-15s: %(levelname)s/%(threadName)s(%(process)d) %(message)s'
LOG_INFO_FORMAT = '%(levelname)s: %(message)s'
LOG_WARNING_FORMAT = '%(message)s'


def set_log_level(level: int) -> None:
    log_format = LOG_WARNING_FORMAT
    if level <= logging.DEBUG:
        log_format = LOG_DEBUG_FORMAT
    elif level <= logging.INFO:
        log_format = LOG_INFO_FORMAT
    logging.basicConfig(level=level, format=log_format)
    logging.getLogger("Rx").setLevel(logging.INFO)
    logging.getLogger('injector').setLevel(logging.INFO)
    logging.getLogger('peewee').setLevel(logging.INFO)
    logging.getLogger('matplotlib').setLevel(logging.INFO)
    logging.getLogger('requests').setLevel(logging.INFO)


_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data_path(path: str) -> str:
    return os.path.join(_ROOT, 'data', path)


def get_config_path(file: str) -> str:
    return os.path.join(BaseDirectory.save_config_path(APP_PACKAGE_NAME), file)


def add_udev_rule() -> int:
    if os.geteuid() == 0:
        if not os.path.isdir(UDEV_RULES_DIR):
            LOG.error("Udev rules have not been added (%s is not a directory)", UDEV_RULES_DIR)
            return 1
        try:
            shutil.copy(get_data_path(UDEV_RULE_FILE_NAME), UDEV_RULES_DIR)
        except IOError:
            LOG.exception("Unable to add udev rule")
            return 1
        try:
            subprocess.call(["udevadm", "control", "--reload-rules"])
            subprocess.call(["udevadm", "trigger", "--subsystem-match=usb", "--attr-match=idVendor=1e71",
                             "--action=add"])
        except OSError:
            LOG.exception("unable to update udev rules (to apply the new rule a reboot may be needed)")
            return 1
        LOG.info("Rule added")
        return 0

    LOG.error("You must have root privileges to modify udev rules. Run this command again using sudo.")
    return 1


def remove_udev_rule() -> int:
    if os.geteuid() == 0:
        path = Path(UDEV_RULES_DIR).joinpath(UDEV_RULE_FILE_NAME)
        if not path.is_file():
            LOG.error("Unable to add udev rule (file %s not found)", str(path))
            return 1
        try:
            path.unlink()
        except IOError:
            LOG.exception("Unable to add udev rule")
            return 1
        try:
            subprocess.call(["udevadm", "control", "--reload-rules"])
            subprocess.call(["udevadm", "trigger", "--subsystem-match=usb", "--attr-match=idVendor=1e71",
                             "--action=add"])
        except OSError:
            LOG.exception("unable to update udev rules (to apply the new rule a reboot may be needed)")
            return 1
        LOG.info("Rule removed")
        return 0

    LOG.error("You must have root privileges to modify udev rules. Run this command again using sudo.")
    return 1
