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

# pylint: disable=too-many-locals,too-many-instance-attributes
from enum import Enum
from typing import Optional

from peewee import Model, CharField, DateTimeField, SqliteDatabase, SQL, IntegerField, Check, \
    ForeignKeyField, BooleanField, BlobField
from playhouse.sqlite_ext import AutoIncrementField

from gkraken.di import INJECTOR


class Status:
    def __init__(self,
                 liquid_temperature: float,
                 fan_rpm: int,
                 pump_rpm: int,
                 firmware_version: str
                 ) -> None:
        self.liquid_temperature: float = liquid_temperature
        self.fan_rpm: int = fan_rpm
        self.fan_speed: Optional[int] = None
        self.pump_rpm: int = pump_rpm
        self.firmware_version: str = firmware_version


class ChannelType(Enum):
    FAN = 'fan'
    PUMP = 'pump'


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


class SpeedStep(Model):
    profile = ForeignKeyField(SpeedProfile, backref='steps')
    temperature = IntegerField()
    duty = IntegerField()
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        legacy_table_names = False
        database = INJECTOR.get(SqliteDatabase)


class CurrentSpeedProfile(Model):
    channel = CharField(primary_key=True, constraints=[Check("channel='%s' OR channel='%s'"
                                                             % (ChannelType.FAN.value, ChannelType.PUMP.value))])
    profile = ForeignKeyField(SpeedProfile, unique=True)
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        legacy_table_names = False
        database = INJECTOR.get(SqliteDatabase)


class Setting(Model):
    key = CharField(primary_key=True)
    value = BlobField()

    class Meta:
        legacy_table_names = False
        database = INJECTOR.get(SqliteDatabase)
