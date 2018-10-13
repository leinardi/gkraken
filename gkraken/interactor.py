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
from distutils.version import LooseVersion
from typing import List, Tuple, Optional

import requests
from injector import singleton, inject
from rx import Observable

from gkraken.conf import SETTINGS_DEFAULTS, APP_PACKAGE_NAME, APP_VERSION
from gkraken.model import Setting
from gkraken.repository import KrakenRepository

LOG = logging.getLogger(__name__)


@singleton
class GetStatusInteractor:
    @inject
    def __init__(self,
                 kraken_repository: KrakenRepository,
                 ) -> None:
        self._kraken_repository = kraken_repository

    def execute(self) -> Observable:
        LOG.debug("GetStatusInteractor.execute()")
        return Observable.defer(lambda: Observable.just(self._kraken_repository.get_status()))


@singleton
class SetSpeedProfileInteractor:
    @inject
    def __init__(self,
                 kraken_repository: KrakenRepository,
                 ) -> None:
        self._kraken_repository = kraken_repository

    def execute(self, channel_value: str, profile_data: List[Tuple[int, int]]) -> Observable:
        LOG.debug("SetSpeedProfileInteractor.execute()")
        return Observable.defer(lambda: Observable.just(
            self._kraken_repository.set_speed_profile(channel_value, profile_data)))


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
    URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'

    @inject
    def __init__(self) -> None:
        pass

    def execute(self) -> Observable:
        LOG.debug("SetSpeedProfileInteractor.execute()")
        return Observable.defer(lambda: Observable.just(self.__check_new_version()))

    def __check_new_version(self) -> Optional[LooseVersion]:
        req = requests.get(self.URL_PATTERN.format(package=APP_PACKAGE_NAME))
        version = LooseVersion("0")
        if req.status_code == requests.codes.ok:
            j = json.loads(req.text)
            releases = j.get('releases', [])
            for release in releases:
                ver = LooseVersion(release)
                version = max(version, ver)
        return version if version > LooseVersion(APP_VERSION) else None
