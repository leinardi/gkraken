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
import json
import logging
import subprocess
from distutils.version import LooseVersion
from typing import List, Tuple, Optional

import requests
import rx
from injector import singleton, inject
from rx import Observable

from gkraken.conf import SETTINGS_DEFAULTS, APP_VERSION, APP_ID
from gkraken.model import Setting
from gkraken.repository import KrakenRepository
from gkraken.util.deployment import is_flatpak

LOG = logging.getLogger(__name__)

_FLATPAK_COMMAND_PREFIX = ['flatpak-spawn', '--host']
_UDEV_RULE = 'SUBSYSTEM=="usb", ATTRS{idVendor}=="1e71", ATTRS{idProduct}=="170e", MODE="0666"'
_UDEV_RULE_FILE_PATH = '/lib/udev/rules.d/60-gkraken.rules'
_UDEV_RULE_RELOAD_COMMANDS = 'udevadm control --reload-rules ' \
                             '&& udevadm trigger --subsystem-match=usb --attr-match=idVendor=1e71 --action=add'


@singleton
class GetStatusInteractor:
    @inject
    def __init__(self,
                 kraken_repository: KrakenRepository,
                 ) -> None:
        self._kraken_repository = kraken_repository

    def execute(self) -> Observable:
        LOG.debug("GetStatusInteractor.execute()")
        return rx.defer(lambda _: rx.just(self._kraken_repository.get_status()))


@singleton
class SetSpeedProfileInteractor:
    @inject
    def __init__(self,
                 kraken_repository: KrakenRepository,
                 ) -> None:
        self._kraken_repository = kraken_repository

    def execute(self, channel_value: str, profile_data: List[Tuple[int, int]]) -> Observable:
        LOG.debug("SetSpeedProfileInteractor.execute()")
        return rx.defer(lambda _: rx.just(self._kraken_repository.set_speed_profile(channel_value, profile_data)))


@singleton
class UdevInteractor:
    @inject
    def __init__(self) -> None:
        pass

    @staticmethod
    def add_udev_rule() -> int:
        cmd = ['pkexec',
               'sh',
               '-c',
               f'echo \'{_UDEV_RULE}\' > {_UDEV_RULE_FILE_PATH} && {_UDEV_RULE_RELOAD_COMMANDS}']
        result = _run_and_get_stdout(cmd)
        if result[0] != 0:
            LOG.warning(f"Error while creating rule file. Exit code: {result[0]}. {result[1]}")
        return result[0]

    @staticmethod
    def remove_udev_rule() -> int:
        cmd = ['pkexec',
               'sh',
               '-c',
               f'rm {_UDEV_RULE_FILE_PATH} && {_UDEV_RULE_RELOAD_COMMANDS}']
        result = _run_and_get_stdout(cmd)
        if result[0] != 0:
            LOG.warning(f"Error while removing rule file. Exit code: {result[0]}. {result[1]}")
        return result[0]


@singleton
class SettingsInteractor:
    @inject
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_bool(key: str, default: Optional[bool] = None) -> bool:
        if default is None:
            default = SETTINGS_DEFAULTS[key]
        setting: Setting = Setting.get_or_none(key=key)
        if setting is not None:
            return bool(setting.value)
        return bool(default)

    @staticmethod
    def set_bool(key: str, value: bool) -> None:
        setting: Setting = Setting.get_or_none(key=key)
        if setting is not None:
            setting.value = value
            setting.save()
        else:
            Setting.create(key=key, value=value)

    @staticmethod
    def get_int(key: str, default: Optional[int] = None) -> int:
        if default is None:
            default = SETTINGS_DEFAULTS[key]
        setting: Setting = Setting.get_or_none(key=key)
        if setting is not None:
            return int(setting.value)
        return default

    @staticmethod
    def set_int(key: str, value: int) -> None:
        setting: Setting = Setting.get_or_none(key=key)
        if setting is not None:
            setting.value = value
            setting.save()
        else:
            Setting.create(key=key, value=value)

    @staticmethod
    def get_str(key: str, default: Optional[str] = None) -> str:
        if default is None:
            default = SETTINGS_DEFAULTS[key]
        setting: Setting = Setting.get_or_none(key=key)
        if setting is not None:
            return str(setting.value.decode("utf-8"))
        return str(default)

    @staticmethod
    def set_str(key: str, value: str) -> None:
        setting: Setting = Setting.get_or_none(key=key)
        if setting is not None:
            setting.value = value.encode("utf-8")
            setting.save()
        else:
            Setting.create(key=key, value=value.encode("utf-8"))


@singleton
class CheckNewVersionInteractor:
    URL_PATTERN = 'https://flathub.org/api/v1/apps/{package}'

    @inject
    def __init__(self) -> None:
        pass

    def execute(self) -> Observable:
        LOG.debug("CheckNewVersionInteractor.execute()")
        return rx.defer(lambda _: rx.just(self._check_new_version()))

    def _check_new_version(self) -> Optional[LooseVersion]:
        req = requests.get(self.URL_PATTERN.format(package=APP_ID))
        version = LooseVersion("0")
        if req.status_code == requests.codes.ok:
            j = json.loads(req.text)
            current_release_version = j.get('currentReleaseVersion', "0.0.0")
            version = LooseVersion(current_release_version)
        return version if version > LooseVersion(APP_VERSION) else None


def _run_and_get_stdout(command: List[str], pipe_command: List[str] = None) -> Tuple[int, str]:
    if pipe_command is None:
        if is_flatpak():
            command = _FLATPAK_COMMAND_PREFIX + command
        process1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = process1.communicate()[0]
        output = output.decode(encoding='UTF-8')
        return process1.returncode, output
    if is_flatpak():
        command = _FLATPAK_COMMAND_PREFIX + command
        pipe_command = _FLATPAK_COMMAND_PREFIX + pipe_command
    process1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    process2 = subprocess.Popen(pipe_command, stdin=process1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process1.stdout.close()
    output = process2.communicate()[0]
    output = output.decode(encoding='UTF-8')
    return process2.returncode, output
