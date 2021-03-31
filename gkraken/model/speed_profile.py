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

import logging
from typing import Any

from peewee import CharField, Check, BooleanField, DateTimeField, SQL, SqliteDatabase
from playhouse.signals import Model, post_save, post_delete
from playhouse.sqlite_ext import AutoIncrementField

from gkraken.di import INJECTOR, SpeedProfileChangedSubject
from gkraken.model.channel_type import ChannelType
from gkraken.model.db_change import DbChange

_LOG = logging.getLogger(__name__)
SPEED_PROFILE_CHANGED_SUBJECT = INJECTOR.get(SpeedProfileChangedSubject)


class SpeedProfile(Model):
    id = AutoIncrementField()
    channel = CharField(constraints=[Check("channel='%s' OR channel='%s'"
                                           % (ChannelType.FAN.value, ChannelType.PUMP.value))])
    name = CharField()
    read_only = BooleanField(default=False)
    single_step = BooleanField(default=False)
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        legacy_table_names = False
        database = INJECTOR.get(SqliteDatabase)


@post_save(sender=SpeedProfile)
def on_speed_profile_added(_: Any, profile: SpeedProfile, created: bool) -> None:
    _LOG.debug("Profile added")
    SPEED_PROFILE_CHANGED_SUBJECT.on_next(DbChange(profile, DbChange.INSERT if created else DbChange.UPDATE))


@post_delete(sender=SpeedProfile)
def on_speed_profile_deleted(_: Any, profile: SpeedProfile) -> None:
    _LOG.debug("Profile deleted")
    SPEED_PROFILE_CHANGED_SUBJECT.on_next(DbChange(profile, DbChange.DELETE))
