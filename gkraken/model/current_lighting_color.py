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

from peewee import CharField, Check, DateTimeField, SQL, SqliteDatabase, IntegerField, CompositeKey
from playhouse.signals import Model

from gkraken.di import INJECTOR
from gkraken.model.lighting_settings import LightingChannel


class CurrentLightingColor(Model):
    channel = CharField(
        constraints=[
            Check("channel='%s' OR channel='%s'" % (LightingChannel.RING.value, LightingChannel.LOGO.value))])
    index = IntegerField()
    red = IntegerField()
    green = IntegerField()
    blue = IntegerField()
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        primary_key = CompositeKey('channel', 'index')
        legacy_table_names = False
        database = INJECTOR.get(SqliteDatabase)
