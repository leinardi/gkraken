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
import logging
from typing import Optional, Any

from gi.repository import Gtk
from injector import singleton, inject

from gkraken.conf import MIN_TEMP, FAN_MIN_DUTY, PUMP_MIN_DUTY, MAX_TEMP, MAX_DUTY, APP_MAIN_UI_NAME
from gkraken.di import EditSpeedProfileBuilder
from gkraken.model import SpeedProfile, SpeedStep, ChannelType
from gkraken.presenter_edit_speed_profile import EditSpeedProfileViewInterface, EditSpeedProfilePresenter
from gkraken.util import  get_data_path

LOG = logging.getLogger(__name__)


@singleton
class EditSpeedProfileView(EditSpeedProfileViewInterface):
    @inject
    def __init__(self,
                 presenter: EditSpeedProfilePresenter,
                 builder: EditSpeedProfileBuilder,
                 ) -> None:
        LOG.debug('init EditSpeedProfileView')
        self._presenter: EditSpeedProfilePresenter = presenter
        self._presenter._view = self
        self._builder: Gtk.Builder = builder
        self._builder.connect_signals(self._presenter)
        self._builder.add_from_file(get_data_path(APP_MAIN_UI_NAME))
        self._dialog: Gtk.Dialog = self._builder.get_object('dialog')
        self._save_profile_button: Gtk.Button = self._builder \
            .get_object('save_profile_button')
        self._delete_profile_button: Gtk.Button = self._builder \
            .get_object('delete_profile_button')
        self._profile_name_entry: Gtk.Entry = self._builder \
            .get_object('profile_name_entry')
        self._liststore: Gtk.ListStore = self._builder.get_object('liststore')
        self._temperature_adjustment: Gtk.Adjustment = self._builder \
            .get_object('temperature_adjustment')
        self._duty_adjustment: Gtk.Adjustment = self._builder \
            .get_object('duty_adjustment')
        self._temperature_scale: Gtk.Scale = self._builder \
            .get_object('temperature_scale')
        self._duty_scale: Gtk.Scale = self._builder \
            .get_object('duty_scale')
        self._controls_grid: Gtk.Grid = self._builder.get_object('controls_grid')
        self._treeselection: Gtk.TreeSelection = self._builder.get_object('treeselection')
        self._add_step_button: Gtk.Button = self._builder.get_object('add_step_button')
        self._save_step_button: Gtk.Button = self._builder \
            .get_object('save_step_button')
        self._delete_step_button: Gtk.Button = self._builder \
            .get_object('delete_step_button')

    def show(self, profile: Optional[SpeedProfile] = None, channel: Optional[ChannelType] = None) -> None:
        self._treeselection.unselect_all()
        if profile is None and channel is None:
            raise ValueError("Both arguments are None")

        if profile is None:
            self._save_profile_button.set_visible(True)
            self._delete_profile_button.set_visible(False)
        else:
            self._save_profile_button.set_visible(False)
            self._delete_profile_button.set_visible(True)
            self._profile_name_entry.set_text(profile.name)
            self.refresh_liststore(profile)
        self.refresh_controls()
        self._dialog.show()

    def hide(self) -> None:
        self._dialog.hide()

    def get_profile_name(self) -> str:
        return str(self._profile_name_entry.get_text())

    def get_temperature(self) -> int:
        return int(self._temperature_adjustment.get_value())

    def get_duty(self) -> int:
        return int(self._duty_adjustment.get_value())

    def refresh_liststore(self, profile: SpeedProfile) -> None:
        self._liststore.clear()
        for step in profile.steps:
            self._liststore.append([step.id, step.temperature, step.duty])

        if profile.steps:
            self._save_profile_button.set_sensitive(True)
            if profile.steps[-1].temperature == MAX_TEMP or profile.steps[-1].duty == MAX_DUTY:
                self._add_step_button.set_sensitive(False)
            else:
                self._add_step_button.set_sensitive(True)
        else:
            self._save_profile_button.set_sensitive(False)

    def refresh_controls(self, step: Optional[SpeedStep] = None, unselect_list: bool = False) -> None:
        if unselect_list:
            self._treeselection.unselect_all()
        if step is None:
            self._controls_grid.set_sensitive(False)
        else:
            prev_steps = (SpeedStep
                          .select()
                          .where(SpeedStep.profile == step.profile, SpeedStep.temperature < step.temperature)
                          .order_by(SpeedStep.temperature.desc())
                          .limit(1))
            next_steps = (SpeedStep
                          .select()
                          .where(SpeedStep.profile == step.profile, SpeedStep.temperature > step.temperature)
                          .order_by(SpeedStep.temperature)
                          .limit(1))
            if len(prev_steps) == 0:
                self._temperature_adjustment.set_lower(MIN_TEMP)
                if step.profile.channel == ChannelType.FAN.value:
                    self._duty_adjustment.set_lower(FAN_MIN_DUTY)
                elif step.profile.channel == ChannelType.PUMP.value:
                    self._duty_adjustment.set_lower(PUMP_MIN_DUTY)
                else:
                    raise ValueError("Unknown channel: %s" % step.profile.channel)
            else:
                LOG.debug("prev = %s", prev_steps[0].temperature)
                self._temperature_adjustment.set_lower(prev_steps[0].temperature + 1)
                self._duty_adjustment.set_lower(prev_steps[0].duty)

            if len(next_steps) == 0:
                self._temperature_adjustment.set_upper(MAX_TEMP)
                self._duty_adjustment.set_upper(MAX_DUTY)
            else:
                self._temperature_adjustment.set_upper(next_steps[0].temperature - 1)
                self._duty_adjustment.set_upper(next_steps[0].duty)

            self._controls_grid.set_sensitive(True)
            self._save_profile_button.set_sensitive(True)
            self._temperature_scale.clear_marks()
            self._temperature_scale.add_mark(step.temperature, Gtk.PositionType.BOTTOM)
            self._temperature_adjustment.set_value(step.temperature)
            self._duty_scale.clear_marks()
            self._duty_scale.add_mark(step.duty, Gtk.PositionType.BOTTOM)
            self._duty_adjustment.set_value(step.duty)
