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
from typing import List, Tuple

from injector import singleton, inject
from rx import Observable

from gkraken.repository import KrakenRepository

LOG = logging.getLogger(__name__)


@singleton
class GetStatusInteractor:
    @inject
    def __init__(self,
                 kraken_repository: KrakenRepository,
                 ) -> None:
        self.__kraken_repository = kraken_repository

    def execute(self) -> Observable:
        LOG.debug("GetStatusInteractor.execute()")
        return Observable.defer(lambda: Observable.just(self.__kraken_repository.get_status()))


@singleton
class SetSpeedProfileInteractor:
    @inject
    def __init__(self,
                 kraken_repository: KrakenRepository,
                 ) -> None:
        self.__kraken_repository = kraken_repository

    def execute(self, channel: str, profile: List[Tuple[int, int]]) -> Observable:
        LOG.debug("SetSpeedProfileInteractor.execute()")
        return Observable.defer(lambda: Observable.just(self.__kraken_repository.set_speed_profile(channel, profile)))
