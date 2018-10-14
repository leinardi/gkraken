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

from gkraken.conf import MIN_TEMP, FAN_MIN_DUTY, PUMP_MIN_DUTY, MAX_TEMP, MAX_DUTY
from gkraken.model import SpeedProfile, SpeedStep, ChannelType
from gkraken.presenter import EditSpeedProfileViewInterface, Presenter
from gkraken.util import hide_on_delete

LOG = logging.getLogger(__name__)


@singleton
class EditSpeedProfileView(EditSpeedProfileViewInterface):
    @inject
    def __init__(self,
                 presenter: Presenter,
                 builder: Gtk.Builder,
                 ) -> None:
        LOG.debug('init EditSpeedProfileView')
        self._presenter: Presenter = presenter
        self._presenter.edit_speed_profile_view = self
        self._builder: Gtk.Builder = builder
        self._profile: Optional[SpeedProfile] = None
        self._selected_step: Optional[SpeedStep] = None
        self._channel_name: str = ""
        self._dialog: Gtk.Dialog = self._builder.get_object('cooling_edit_speed_dialog')
        self._dialog.connect("delete-event", self.on_delete_event)
        self._save_profile_button: Gtk.Button = self._builder \
            .get_object('cooling_edit_speed_save_profile_button')
        self._delete_profile_button: Gtk.Button = self._builder \
            .get_object('cooling_edit_speed_delete_profile_button')
        self._profile_name_entry: Gtk.Entry = self._builder \
            .get_object('cooling_edit_speed_profile_name_entry')
        self._liststore: Gtk.ListStore = self._builder.get_object('cooling_edit_speed_liststore')
        self._temperature_adjustment: Gtk.Adjustment = self._builder \
            .get_object('cooling_edit_speed_temperature_adjustment')
        self._duty_adjustment: Gtk.Adjustment = self._builder \
            .get_object('cooling_edit_speed_duty_adjustment')
        self._temperature_scale: Gtk.Scale = self._builder \
            .get_object('cooling_edit_speed_temperature_scale')
        self._duty_scale: Gtk.Scale = self._builder \
            .get_object('cooling_edit_speed_duty_scale')
        self._controls_grid: Gtk.Grid = self._builder.get_object('cooling_edit_speed_controls_grid')
        self._treeselection: Gtk.TreeSelection = self._builder.get_object('cooling_edit_speed_treeselection')
        self._treeselection.connect("changed", self.on_step_selected)
        self._add_step_button: Gtk.Button = self._builder.get_object('cooling_edit_speed_add_step_button')
        self._add_step_button.connect('clicked', self.on_add_step_clicked)
        self._save_step_button: Gtk.Button = self._builder \
            .get_object('cooling_edit_speed_save_step_button')
        self._delete_step_button: Gtk.Button = self._builder \
            .get_object('cooling_edit_speed_delete_step_button')
        delete_profile_button: Gtk.Button = self._builder \
            .get_object('cooling_edit_speed_delete_profile_button')
        delete_profile_button.connect('clicked', self.on_delete_profile_clicked)
        delete_step_button: Gtk.Button = self._builder \
            .get_object('cooling_edit_speed_delete_step_button')
        delete_step_button.connect('clicked', self.on_delete_step_clicked)
        save_step_button: Gtk.Button = self._builder \
            .get_object('cooling_edit_speed_save_step_button')
        save_step_button.connect('clicked', self.on_save_step_clicked)

    def on_delete_event(self, widget: Gtk.Widget, *_: Any) -> Any:
        if self._profile is not None:
            if self._profile_name_entry.get_text() != self._profile.name:
                self._profile.name = self._profile_name_entry.get_text()
                self._profile.save()
        return hide_on_delete(widget)

    def show(self, profile: Optional[SpeedProfile] = None, channel: Optional[ChannelType] = None) -> None:
        self._treeselection.unselect_all()
        if profile is None and channel is None:
            raise ValueError("Both arguments are None")

        if profile is None:
            self._channel_name = channel.value
            self._save_profile_button.set_visible(True)
            self._delete_profile_button.set_visible(False)
        else:
            self._profile = profile
            self._channel_name = profile.channel
            self._save_profile_button.set_visible(False)
            self._delete_profile_button.set_visible(True)
            self._profile_name_entry.set_text(profile.name)
            self._refresh_liststore(profile)
        self._refresh_controls()
        self._dialog.show()

    def hide(self) -> None:
        self._dialog.hide()

    def on_step_selected(self, tree_selection: Gtk.TreeSelection) -> None:
        LOG.debug("selected")
        list_store, tree_iter = tree_selection.get_selected()
        step = None if tree_iter is None else SpeedStep.get_or_none(id=list_store.get_value(tree_iter, 0))
        self._refresh_controls(step)

    def on_delete_profile_clicked(self, *_: Any) -> None:
        self._profile.delete_instance(recursive=True)
        self.hide()

    def on_add_step_clicked(self, *_: Any) -> None:
        self._treeselection.unselect_all()
        step = SpeedStep()
        step.profile = self._profile
        last_steps = (SpeedStep
                      .select()
                      .where(SpeedStep.profile == step.profile)
                      .order_by(SpeedStep.temperature.desc())
                      .limit(1))
        if len(last_steps) == 0:
            step.temperature = MIN_TEMP
            step.duty = FAN_MIN_DUTY if step.profile.channel == ChannelType.FAN.value else PUMP_MIN_DUTY
        else:
            step.temperature = last_steps[0].temperature + 1
            step.duty = last_steps[0].duty

        self._refresh_controls(step)

    def on_delete_step_clicked(self, *_: Any) -> None:
        self._selected_step.delete_instance()
        self._refresh_liststore(self._profile)

    def on_save_step_clicked(self, *_: Any) -> None:
        self._selected_step.temperature = self._temperature_adjustment.get_value()
        self._selected_step.duty = self._duty_adjustment.get_value()
        self._selected_step.save()
        self._refresh_liststore(self._profile)

    def _refresh_liststore(self, profile: SpeedProfile) -> None:
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

    def _refresh_controls(self, step: Optional[SpeedStep] = None) -> None:
        if step is None:
            self._controls_grid.set_sensitive(False)
        else:
            self._selected_step = step
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
                if self._channel_name == ChannelType.FAN.value:
                    self._duty_adjustment.set_lower(FAN_MIN_DUTY)
                elif self._channel_name == ChannelType.PUMP.value:
                    self._duty_adjustment.set_lower(PUMP_MIN_DUTY)
                else:
                    raise ValueError("Unknown channel: %s" % self._channel_name)
                self._duty_adjustment.set_lower(FAN_MIN_DUTY)
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
