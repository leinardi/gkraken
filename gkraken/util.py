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
from gkraken.model import SpeedProfile, SpeedStep, ChannelType

LOG = logging.getLogger(__name__)


def synchronized_with_attr(lock_name):
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator


def load_db_default_data() -> None:
    fan_silent = SpeedProfile.create(name="Silent", channel=ChannelType.FAN.value, read_only=True)
    fan_perf = SpeedProfile.create(name="Performance", channel=ChannelType.FAN.value, read_only=True)
    fan_fixed = SpeedProfile.create(name="Fixed", channel=ChannelType.FAN.value, single_step=True)
    pump_silent = SpeedProfile.create(name="Silent", channel=ChannelType.PUMP.value, read_only=True)
    pump_perf = SpeedProfile.create(name="Performance", channel=ChannelType.PUMP.value, read_only=True)
    pump_fixed = SpeedProfile.create(name="Fixed", channel=ChannelType.PUMP.value, single_step=True)

    # Fan Silent
    SpeedStep.create(
        profile=fan_silent.id,
        temperature=20,
        duty=25)
    SpeedStep.create(
        profile=fan_silent.id,
        temperature=35,
        duty=25)
    SpeedStep.create(
        profile=fan_silent.id,
        temperature=40,
        duty=35)
    SpeedStep.create(
        profile=fan_silent.id,
        temperature=45,
        duty=45)
    SpeedStep.create(
        profile=fan_silent.id,
        temperature=50,
        duty=55)
    SpeedStep.create(
        profile=fan_silent.id,
        temperature=55,
        duty=75)
    SpeedStep.create(
        profile=fan_silent.id,
        temperature=60,
        duty=100)

    # Fan Performance
    SpeedStep.create(
        profile=fan_perf.id,
        temperature=20,
        duty=50)
    SpeedStep.create(
        profile=fan_perf.id,
        temperature=35,
        duty=50)
    SpeedStep.create(
        profile=fan_perf.id,
        temperature=40,
        duty=60)
    SpeedStep.create(
        profile=fan_perf.id,
        temperature=45,
        duty=70)
    SpeedStep.create(
        profile=fan_perf.id,
        temperature=50,
        duty=80)
    SpeedStep.create(
        profile=fan_perf.id,
        temperature=55,
        duty=90)
    SpeedStep.create(
        profile=fan_perf.id,
        temperature=60,
        duty=100)

    # Fan Fixed
    SpeedStep.create(
        profile=fan_fixed.id,
        temperature=20,
        duty=25)

    # Pump Silent
    SpeedStep.create(
        profile=pump_silent.id,
        temperature=20,
        duty=60)
    SpeedStep.create(
        profile=pump_silent.id,
        temperature=35,
        duty=60)
    SpeedStep.create(
        profile=pump_silent.id,
        temperature=40,
        duty=70)
    SpeedStep.create(
        profile=pump_silent.id,
        temperature=45,
        duty=80)
    SpeedStep.create(
        profile=pump_silent.id,
        temperature=50,
        duty=90)
    SpeedStep.create(
        profile=pump_silent.id,
        temperature=55,
        duty=100)
    SpeedStep.create(
        profile=pump_silent.id,
        temperature=60,
        duty=100)

    # Pump Performance
    SpeedStep.create(
        profile=pump_perf.id,
        temperature=20,
        duty=70)
    SpeedStep.create(
        profile=pump_perf.id,
        temperature=35,
        duty=70)
    SpeedStep.create(
        profile=pump_perf.id,
        temperature=40,
        duty=80)
    SpeedStep.create(
        profile=pump_perf.id,
        temperature=45,
        duty=85)
    SpeedStep.create(
        profile=pump_perf.id,
        temperature=50,
        duty=90)
    SpeedStep.create(
        profile=pump_perf.id,
        temperature=55,
        duty=95)
    SpeedStep.create(
        profile=pump_perf.id,
        temperature=60,
        duty=100)

    # Pump Fixed
    SpeedStep.create(
        profile=pump_fixed.id,
        temperature=20,
        duty=60)
