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
from gkraken.conf import FAN_MIN_DUTY, PUMP_MIN_DUTY
from gkraken.model.channel_type import ChannelType
from gkraken.model.speed_profile import SpeedProfile
from gkraken.model.speed_step import SpeedStep


def load_db_default_data() -> None:
    fan_silent = SpeedProfile.create(name="Silent",
                                     channel=ChannelType.FAN.value, read_only=True)
    fan_perf = SpeedProfile.create(name="Performance", channel=ChannelType.FAN.value, read_only=True)
    fan_fixed = SpeedProfile.create(name="Fixed", channel=ChannelType.FAN.value, single_step=True)
    pump_silent = SpeedProfile.create(name="Silent", channel=ChannelType.PUMP.value, read_only=True)
    pump_perf = SpeedProfile.create(name="Performance", channel=ChannelType.PUMP.value, read_only=True)
    pump_fixed = SpeedProfile.create(name="Fixed", channel=ChannelType.PUMP.value, single_step=True)

    # Fan Silent
    SpeedStep.create(profile=fan_silent.id, temperature=20, duty=25)
    SpeedStep.create(profile=fan_silent.id, temperature=35, duty=25)
    SpeedStep.create(profile=fan_silent.id, temperature=50, duty=55)
    SpeedStep.create(profile=fan_silent.id, temperature=60, duty=100)

    # Fan Performance
    SpeedStep.create(profile=fan_perf.id, temperature=20, duty=50)
    SpeedStep.create(profile=fan_perf.id, temperature=35, duty=50)
    SpeedStep.create(profile=fan_perf.id, temperature=60, duty=100)

    # Fan Fixed
    SpeedStep.create(profile=fan_fixed.id, temperature=20, duty=FAN_MIN_DUTY)

    # Pump Silent
    SpeedStep.create(profile=pump_silent.id, temperature=20, duty=60)
    SpeedStep.create(profile=pump_silent.id, temperature=35, duty=60)
    SpeedStep.create(profile=pump_silent.id, temperature=55, duty=100)
    SpeedStep.create(profile=pump_silent.id, temperature=60, duty=100)

    # Pump Performance
    SpeedStep.create(profile=pump_perf.id, temperature=20, duty=70)
    SpeedStep.create(profile=pump_perf.id, temperature=35, duty=70)
    SpeedStep.create(profile=pump_perf.id, temperature=40, duty=80)
    SpeedStep.create(profile=pump_perf.id, temperature=60, duty=100)

    # Pump Fixed
    SpeedStep.create(profile=pump_fixed.id, temperature=20, duty=PUMP_MIN_DUTY)
