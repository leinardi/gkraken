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
from gkraken.model import TemperatureDutyProfileDbModel, TemperatureDutyStepDbModel, FAN_CHANNEL, PUMP_CHANNEL

LOG = logging.getLogger(__name__)


def load_db_default_data() -> None:
    fan_silent = TemperatureDutyProfileDbModel.create(name="Silent", channel=FAN_CHANNEL, read_only=True)
    fan_perf = TemperatureDutyProfileDbModel.create(name="Performance", channel=FAN_CHANNEL, read_only=True)
    fan_fixed = TemperatureDutyProfileDbModel.create(name="Fixed", channel=FAN_CHANNEL, single_step=True)
    pump_silent = TemperatureDutyProfileDbModel.create(name="Silent", channel=PUMP_CHANNEL, read_only=True)
    pump_perf = TemperatureDutyProfileDbModel.create(name="Performance", channel=PUMP_CHANNEL, read_only=True)
    pump_fixed = TemperatureDutyProfileDbModel.create(name="Fixed", channel=PUMP_CHANNEL, single_step=True)

    # Fan Silent
    TemperatureDutyStepDbModel.create(
        profile=fan_silent.id,
        temperature=20,
        duty=25)
    TemperatureDutyStepDbModel.create(
        profile=fan_silent.id,
        temperature=40,
        duty=35)
    TemperatureDutyStepDbModel.create(
        profile=fan_silent.id,
        temperature=45,
        duty=45)
    TemperatureDutyStepDbModel.create(
        profile=fan_silent.id,
        temperature=50,
        duty=55)
    TemperatureDutyStepDbModel.create(
        profile=fan_silent.id,
        temperature=55,
        duty=75)
    TemperatureDutyStepDbModel.create(
        profile=fan_silent.id,
        temperature=60,
        duty=100)

    # Fan Performance
    TemperatureDutyStepDbModel.create(
        profile=fan_perf.id,
        temperature=20,
        duty=50)
    TemperatureDutyStepDbModel.create(
        profile=fan_perf.id,
        temperature=40,
        duty=60)
    TemperatureDutyStepDbModel.create(
        profile=fan_perf.id,
        temperature=45,
        duty=70)
    TemperatureDutyStepDbModel.create(
        profile=fan_perf.id,
        temperature=50,
        duty=80)
    TemperatureDutyStepDbModel.create(
        profile=fan_perf.id,
        temperature=55,
        duty=90)
    TemperatureDutyStepDbModel.create(
        profile=fan_perf.id,
        temperature=60,
        duty=100)

    # Fan Fixed
    TemperatureDutyStepDbModel.create(
        profile=fan_fixed.id,
        temperature=20,
        duty=25)

    # Pump Silent
    TemperatureDutyStepDbModel.create(
        profile=pump_silent.id,
        temperature=20,
        duty=60)
    TemperatureDutyStepDbModel.create(
        profile=pump_silent.id,
        temperature=40,
        duty=70)
    TemperatureDutyStepDbModel.create(
        profile=pump_silent.id,
        temperature=45,
        duty=80)
    TemperatureDutyStepDbModel.create(
        profile=pump_silent.id,
        temperature=50,
        duty=90)
    TemperatureDutyStepDbModel.create(
        profile=pump_silent.id,
        temperature=55,
        duty=100)
    TemperatureDutyStepDbModel.create(
        profile=pump_silent.id,
        temperature=60,
        duty=100)

    # Pump Performance
    TemperatureDutyStepDbModel.create(
        profile=pump_perf.id,
        temperature=20,
        duty=70)
    TemperatureDutyStepDbModel.create(
        profile=pump_perf.id,
        temperature=40,
        duty=80)
    TemperatureDutyStepDbModel.create(
        profile=pump_perf.id,
        temperature=45,
        duty=85)
    TemperatureDutyStepDbModel.create(
        profile=pump_perf.id,
        temperature=50,
        duty=90)
    TemperatureDutyStepDbModel.create(
        profile=pump_perf.id,
        temperature=55,
        duty=95)
    TemperatureDutyStepDbModel.create(
        profile=pump_perf.id,
        temperature=60,
        duty=100)

    # Pump Fixed
    TemperatureDutyStepDbModel.create(
        profile=pump_fixed.id,
        temperature=20,
        duty=60)
