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
from peewee import CharField, Check, ForeignKeyField, DateTimeField, SQL, SqliteDatabase
from playhouse.signals import Model

from gkraken.di import INJECTOR
from gkraken.model.channel_type import ChannelType
from gkraken.model.speed_profile import SpeedProfile


class CurrentSpeedProfile(Model):
    channel = CharField(primary_key=True, constraints=[Check("channel='%s' OR channel='%s'"
                                                             % (ChannelType.FAN.value, ChannelType.PUMP.value))])
    profile = ForeignKeyField(SpeedProfile, unique=True)
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        legacy_table_names = False
        database = INJECTOR.get(SqliteDatabase)
