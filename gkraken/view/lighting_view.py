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
from typing import List

from injector import singleton, inject
from gi.repository import Gtk

from gkraken.di import MainBuilder
from gkraken.model.lighting_modes import LightingMode, LightingModes
from gkraken.model.lighting_settings import LightingDirection, LightingColors, LightingColor
from gkraken.model.lighting_speeds import LightingSpeeds
from gkraken.presenter.main_presenter import MainPresenter, LightingViewInterface

_LOG = logging.getLogger(__name__)


@singleton
class LightingView(LightingViewInterface):

    @inject
    def __init__(self,
                 presenter: MainPresenter,
                 builder: MainBuilder,
                 ) -> None:
        _LOG.debug('init LightingView')
        self._presenter: MainPresenter = presenter
        self._presenter.lighting_view = self
        self._builder: Gtk.Builder = builder
        self._lighting_logo_button_list: List[Gtk.ColorButton] = []
        self._lighting_ring_button_list: List[Gtk.ColorButton] = []
        self._init_lighting_widgets()
        self._init_button_lists()

    def _init_lighting_widgets(self) -> None:
        self._lighting_logo_mode_liststore: Gtk.ListStore = self._builder.get_object('lighting_logo_mode_liststore')
        self._lighting_logo_mode_combobox: Gtk.ListStore = self._builder.get_object('lighting_logo_mode_combobox')
        self._lighting_logo_speed_liststore: Gtk.ListStore = self._builder.get_object('lighting_logo_speed_liststore')
        self._lighting_logo_speed_combobox: Gtk.ListStore = self._builder.get_object('lighting_logo_speed_combobox')
        self._lighting_logo_direction_reverse: Gtk.ToggleButton = \
            self._builder.get_object('lighting_logo_direction_reverse')
        self._lighting_logo_color_1: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_1')
        self._lighting_logo_color_2: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_2')
        self._lighting_logo_color_3: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_3')
        self._lighting_logo_color_4: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_4')
        self._lighting_logo_color_5: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_5')
        self._lighting_logo_color_6: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_6')
        self._lighting_logo_color_7: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_7')
        self._lighting_logo_color_8: Gtk.ColorButton = self._builder.get_object('lighting_logo_color_8')
        self._lighting_logo_colors_spinbutton: Gtk.SpinButton = \
            self._builder.get_object('lighting_logo_colors_spinbutton')
        self._lighting_logo_colors_spinbutton_adjustment: Gtk.Adjustment = \
            self._builder.get_object('lighting_logo_colors_spinbutton_adjustment')
        self._lighting_ring_mode_liststore: Gtk.ListStore = self._builder.get_object('lighting_ring_mode_liststore')
        self._lighting_ring_mode_combobox: Gtk.ListStore = self._builder.get_object('lighting_ring_mode_combobox')
        self._lighting_ring_speed_liststore: Gtk.ListStore = self._builder.get_object('lighting_ring_speed_liststore')
        self._lighting_ring_speed_combobox: Gtk.ListStore = self._builder.get_object('lighting_ring_speed_combobox')
        self._lighting_ring_direction_reverse: Gtk.ToggleButton = \
            self._builder.get_object('lighting_ring_direction_reverse')
        self._lighting_ring_color_1: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_1')
        self._lighting_ring_color_2: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_2')
        self._lighting_ring_color_3: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_3')
        self._lighting_ring_color_4: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_4')
        self._lighting_ring_color_5: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_5')
        self._lighting_ring_color_6: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_6')
        self._lighting_ring_color_7: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_7')
        self._lighting_ring_color_8: Gtk.ColorButton = self._builder.get_object('lighting_ring_color_8')
        self._lighting_ring_colors_spinbutton: Gtk.SpinButton = \
            self._builder.get_object('lighting_ring_colors_spinbutton')
        self._lighting_ring_colors_spinbutton_adjustment: Gtk.Adjustment = \
            self._builder.get_object('lighting_ring_colors_spinbutton_adjustment')
        self._lighting_apply_button: Gtk.Button = self._builder.get_object('lighting_apply_button')

    def _init_button_lists(self) -> None:
        self._lighting_logo_button_list: List[Gtk.ColorButton] = [
            self._lighting_logo_color_1, self._lighting_logo_color_2, self._lighting_logo_color_3,
            self._lighting_logo_color_4, self._lighting_logo_color_5, self._lighting_logo_color_6,
            self._lighting_logo_color_7, self._lighting_logo_color_8
        ]
        self._lighting_ring_button_list: List[Gtk.ColorButton] = [
        self._lighting_ring_color_1, self._lighting_ring_color_2, self._lighting_ring_color_3,
        self._lighting_ring_color_4, self._lighting_ring_color_5, self._lighting_ring_color_6,
        self._lighting_ring_color_7, self._lighting_ring_color_8
        ]

    def load_color_modes(self, lighting_modes: LightingModes) -> None:
        for mode_id, lighting_mode in lighting_modes.modes_logo.items():
            self._lighting_logo_mode_liststore.append([mode_id, lighting_mode.frontend_name])
        for mode_id, lighting_mode in lighting_modes.modes_ring.items():
            self._lighting_ring_mode_liststore.append([mode_id, lighting_mode.frontend_name])

        self._lighting_logo_mode_combobox.set_model(self._lighting_logo_mode_liststore)
        self._lighting_logo_mode_combobox.set_sensitive(len(self._lighting_logo_mode_liststore) > 0)
        self._lighting_ring_mode_combobox.set_model(self._lighting_ring_mode_liststore)
        self._lighting_ring_mode_combobox.set_sensitive(len(self._lighting_ring_mode_liststore) > 0)

        for speed in LightingSpeeds().values():
            self._lighting_logo_speed_liststore.append([speed.speed_id, speed.frontend_name])
            self._lighting_ring_speed_liststore.append([speed.speed_id, speed.frontend_name])

        self._lighting_logo_speed_combobox.set_model(self._lighting_logo_speed_liststore)
        self._lighting_logo_speed_combobox.set_active(2)
        self._lighting_ring_speed_combobox.set_model(self._lighting_logo_speed_liststore)
        self._lighting_ring_speed_combobox.set_active(2)

    def set_lighting_apply_button_enabled(self, enabled: bool) -> None:
        self._lighting_apply_button.set_sensitive(enabled)

    def set_lighting_logo_color_buttons_enabled(self, max_colors: int) -> None:
        for index, button in enumerate(self._lighting_logo_button_list):
            button.set_sensitive(index < max_colors)

    def get_logo_mode_id(self) -> int:
        active = self._lighting_logo_mode_combobox.get_active()
        mode_id = self._lighting_logo_mode_combobox.get_model()[active][0] \
            if active >= 0 else -1
        return int(mode_id)

    def get_logo_colors(self, max_colors: int) -> LightingColors:
        colors = LightingColors()
        for index in range(max_colors):
            color = self._lighting_logo_button_list[index].get_rgba()
            colors.add(LightingColor.from_button_color(color))
        return colors

    def set_lighting_logo_spin_button(self, lighting_mode: LightingMode) -> None:
        self._lighting_logo_colors_spinbutton.set_sensitive(
            abs(lighting_mode.min_colors - lighting_mode.max_colors) > 0)
        self._lighting_logo_colors_spinbutton_adjustment.set_lower(lighting_mode.min_colors)
        self._lighting_logo_colors_spinbutton_adjustment.set_upper(lighting_mode.max_colors)
        self._lighting_logo_colors_spinbutton.set_value(lighting_mode.min_colors)

    def get_lighting_logo_spin_button(self) -> int:
        return int(self._lighting_logo_colors_spinbutton.get_value_as_int())

    def set_lighting_logo_speed_enabled(self, enabled: bool) -> None:
        self._lighting_logo_speed_combobox.set_sensitive(enabled)

    def get_lighting_logo_speed(self) -> int:
        active = self._lighting_logo_speed_combobox.get_active()
        speed_id = self._lighting_logo_speed_combobox.get_model()[active][0] \
            if active >= 0 else -1
        return int(speed_id)

    def set_lighting_logo_direction_enabled(self, enabled: bool) -> None:
        self._lighting_logo_direction_reverse.set_sensitive(enabled)

    def get_lighting_logo_direction(self) -> LightingDirection:
        active = self._lighting_logo_direction_reverse.get_active()
        return LightingDirection.BACKWARD if active else LightingDirection.FORWARD

    def get_ring_mode_id(self) -> int:
        active = self._lighting_ring_mode_combobox.get_active()
        mode_id = self._lighting_ring_mode_combobox.get_model()[active][0] \
            if active >= 0 else -1
        return int(mode_id)

    def set_lighting_ring_color_buttons_enabled(self, max_colors: int) -> None:
        for index, button in enumerate(self._lighting_ring_button_list):
            button.set_sensitive(index < max_colors)

    def get_ring_colors(self, max_colors: int) -> LightingColors:
        colors = LightingColors()
        for index in range(max_colors):
            color = self._lighting_ring_button_list[index].get_rgba()
            colors.add(LightingColor.from_button_color(color))
        return colors

    def set_lighting_ring_spin_button(self, lighting_mode: LightingMode) -> None:
        self._lighting_ring_colors_spinbutton.set_sensitive(
            abs(lighting_mode.min_colors - lighting_mode.max_colors) > 0)
        self._lighting_ring_colors_spinbutton_adjustment.set_lower(lighting_mode.min_colors)
        self._lighting_ring_colors_spinbutton_adjustment.set_upper(lighting_mode.max_colors)
        self._lighting_ring_colors_spinbutton.set_value(lighting_mode.min_colors)

    def get_lighting_ring_spin_button(self) -> int:
        return int(self._lighting_ring_colors_spinbutton.get_value_as_int())

    def set_lighting_ring_speed_enabled(self, enabled: bool) -> None:
        self._lighting_ring_speed_combobox.set_sensitive(enabled)

    def get_lighting_ring_speed(self) -> int:
        active = self._lighting_ring_speed_combobox.get_active()
        speed_id = self._lighting_ring_speed_combobox.get_model()[active][0] \
            if active >= 0 else -1
        return int(speed_id)

    def set_lighting_ring_direction_enabled(self, enabled: bool) -> None:
        self._lighting_ring_direction_reverse.set_sensitive(enabled)

    def get_lighting_ring_direction(self) -> LightingDirection:
        active = self._lighting_ring_direction_reverse.get_active()
        return LightingDirection.BACKWARD if active else LightingDirection.FORWARD
