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
from typing import Optional, Any

from gi.repository import Gtk
from injector import singleton, inject

from gkraken.conf import MIN_TEMP, PUMP_MIN_DUTY, FAN_MIN_DUTY
from gkraken.model import SpeedProfile, ChannelType, SpeedStep
from gkraken.util.view import hide_on_delete

_LOG = logging.getLogger(__name__)


class EditSpeedProfileViewInterface:
    def show(self, profile: SpeedProfile) -> None:
        raise NotImplementedError()

    def hide(self) -> None:
        raise NotImplementedError()

    def get_profile_name(self) -> str:
        raise NotImplementedError()

    def get_temperature(self) -> int:
        raise NotImplementedError()

    def get_duty(self) -> int:
        raise NotImplementedError()

    def has_a_step_selected(self) -> bool:
        raise NotImplementedError()

    def refresh_controls(self, step: Optional[SpeedStep] = None, unselect_list: bool = False) -> None:
        raise NotImplementedError()

    def refresh_liststore(self, profile: SpeedProfile) -> None:
        raise NotImplementedError()


@singleton
class EditSpeedProfilePresenter:
    @inject
    def __init__(self) -> None:
        _LOG.debug("init EditSpeedProfilePresenter ")
        self.view: EditSpeedProfileViewInterface = EditSpeedProfileViewInterface()
        self._profile = SpeedProfile()
        self._selected_step: Optional[SpeedStep] = None
        self._channel_name: str = ""

    def show_add(self, channel: ChannelType) -> None:
        self._channel_name = channel.value
        profile = SpeedProfile()
        profile.name = 'New profile'
        profile.channel = channel.value
        profile.save()
        self.show_edit(profile)

    def show_edit(self, profile: SpeedProfile) -> None:
        self._channel_name = profile.channel
        self._profile = profile
        self.view.show(profile)

    def on_dialog_delete_event(self, widget: Gtk.Widget, *_: Any) -> Any:
        if self._profile is not None:
            name = self.view.get_profile_name()
            if name != self._profile.name:
                self._profile.name = name
                self._profile.save()
        return hide_on_delete(widget)

    def refresh_controls(self, step: Optional[SpeedStep] = None, unselect_list: bool = False) -> None:
        self._selected_step = step
        self.view.refresh_controls(step, unselect_list)

    def on_step_selected(self, tree_selection: Gtk.TreeSelection) -> None:
        _LOG.debug("selected")
        list_store, tree_iter = tree_selection.get_selected()
        step = None if tree_iter is None else SpeedStep.get_or_none(id=list_store.get_value(tree_iter, 0))
        self.refresh_controls(step)

    def on_add_step_clicked(self, *_: Any) -> None:
        step = SpeedStep()
        step.profile = self._profile
        last_steps = (SpeedStep
                      .select()
                      .where(SpeedStep.profile == step.profile)
                      .order_by(SpeedStep.temperature.desc())
                      .limit(1))
        if not last_steps:
            step.temperature = MIN_TEMP
            step.duty = FAN_MIN_DUTY if step.profile.channel == ChannelType.FAN.value else PUMP_MIN_DUTY
        else:
            step.temperature = last_steps[0].temperature + 1
            step.duty = last_steps[0].duty

        self.refresh_controls(step, True)

    def on_add_profile_clicked(self, *_: Any) -> None:
        self._profile.delete_instance(recursive=True)
        self.view.hide()

    def on_delete_profile_clicked(self, *_: Any) -> None:
        self._profile.delete_instance(recursive=True)
        self.view.hide()

    def on_delete_step_clicked(self, *_: Any) -> None:
        self._selected_step.delete_instance()  # type: ignore[union-attr]
        self.view.refresh_liststore(self._profile)

    def on_save_step_clicked(self, *_: Any) -> None:
        self._selected_step.temperature = self.view.get_temperature()  # type: ignore[union-attr]
        self._selected_step.duty = self.view.get_duty()  # type: ignore[union-attr]
        self._selected_step.save()  # type: ignore[union-attr]
        self.view.refresh_liststore(self._profile)
        if not self.view.has_a_step_selected():
            self.refresh_controls()
