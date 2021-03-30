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

from gi.repository import Gtk
from injector import singleton, inject

from gkraken.conf import APP_PACKAGE_NAME
from gkraken.di import MainBuilder
from gkraken.model.lighting_modes import LightingMode, LightingModes
from gkraken.model.lighting_settings import LightingDirection, LightingColors, LightingColor
from gkraken.model.lighting_speeds import LightingSpeeds
from gkraken.presenter.lighting_presenter import LightingPresenter
from gkraken.view.lighting_view_interface import LightingViewInterface

_LOG = logging.getLogger(__name__)


@singleton
class LightingView(LightingViewInterface):

    @inject
    def __init__(self,
                 presenter: LightingPresenter,
                 builder: MainBuilder,
                 ) -> None:
        _LOG.debug('init LightingView')
        self._presenter: LightingPresenter = presenter
        self._presenter.view = self
        self._builder: Gtk.Builder = builder
        self._lighting_logo_button_list: List[Gtk.ColorButton] = []
        self._lighting_ring_button_list: List[Gtk.ColorButton] = []
        self._init_lighting_widgets()
        self._init_button_lists()

    def _init_lighting_widgets(self) -> None:
        self._statusbar: Gtk.Statusbar = self._builder.get_object('statusbar')
        self._context = self._statusbar.get_context_id(APP_PACKAGE_NAME)
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
            self._lighting_logo_mode_liststore.append([str(mode_id), lighting_mode.frontend_name])
        for mode_id, lighting_mode in lighting_modes.modes_ring.items():
            self._lighting_ring_mode_liststore.append([str(mode_id), lighting_mode.frontend_name])

        self._lighting_logo_mode_combobox.set_model(self._lighting_logo_mode_liststore)
        self._lighting_logo_mode_combobox.set_sensitive(len(self._lighting_logo_mode_liststore) > 0)
        self._lighting_ring_mode_combobox.set_model(self._lighting_ring_mode_liststore)
        self._lighting_ring_mode_combobox.set_sensitive(len(self._lighting_ring_mode_liststore) > 0)

        for speed in LightingSpeeds().values():
            self._lighting_logo_speed_liststore.append([str(speed.id), speed.frontend_name])
            self._lighting_ring_speed_liststore.append([str(speed.id), speed.frontend_name])

        self._lighting_logo_speed_combobox.set_model(self._lighting_logo_speed_liststore)
        self._lighting_logo_speed_combobox.set_active(2)
        self._lighting_ring_speed_combobox.set_model(self._lighting_logo_speed_liststore)
        self._lighting_ring_speed_combobox.set_active(2)

        self.set_lighting_logo_color_buttons_enabled(0)
        self.set_lighting_ring_color_buttons_enabled(0)
        _LOG.debug("All lighting modes loaded")

    def set_statusbar_text(self, text: str) -> None:
        self._statusbar.remove_all(self._context)
        self._statusbar.push(self._context, text)

    def set_lighting_apply_button_enabled(self, enabled: bool) -> None:
        self._lighting_apply_button.set_sensitive(enabled)

    def set_lighting_logo_color_buttons_enabled(self, max_colors: int) -> None:
        for index, button in enumerate(self._lighting_logo_button_list):
            is_enabled = index < max_colors
            button.set_visible(is_enabled)
            button.set_sensitive(is_enabled)

    def get_logo_mode_id(self) -> int:
        active_mode_id = self._lighting_logo_mode_combobox.get_active_id()
        return int(active_mode_id) if active_mode_id else -1

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
        active_speed_id = self._lighting_logo_speed_combobox.get_active_id()
        return int(active_speed_id) if active_speed_id else -1

    def set_lighting_logo_direction_enabled(self, enabled: bool) -> None:
        self._lighting_logo_direction_reverse.set_sensitive(enabled)

    def get_lighting_logo_direction(self) -> LightingDirection:
        active = self._lighting_logo_direction_reverse.get_active()
        return LightingDirection.BACKWARD if active else LightingDirection.FORWARD

    def get_ring_mode_id(self) -> int:
        active_mode_id = self._lighting_ring_mode_combobox.get_active_id()
        return int(active_mode_id) if active_mode_id else -1

    def set_lighting_ring_color_buttons_enabled(self, max_colors: int) -> None:
        for index, button in enumerate(self._lighting_ring_button_list):
            is_enabled = index < max_colors
            button.set_visible(is_enabled)
            button.set_sensitive(is_enabled)

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
        active_speed_id = self._lighting_ring_speed_combobox.get_active()
        return int(active_speed_id) if active_speed_id else -1

    def set_lighting_ring_direction_enabled(self, enabled: bool) -> None:
        self._lighting_ring_direction_reverse.set_sensitive(enabled)

    def get_lighting_ring_direction(self) -> LightingDirection:
        active = self._lighting_ring_direction_reverse.get_active()
        return LightingDirection.BACKWARD if active else LightingDirection.FORWARD

    def set_logo_mode_id(self, mode_id: int) -> None:
        self._lighting_logo_mode_combobox.set_active_id(str(mode_id))

    def set_logo_speed_id(self, speed_id: int) -> None:
        self._lighting_logo_speed_combobox.set_active_id(str(speed_id))

    def set_logo_direction(self, direction: LightingDirection) -> None:
        self._lighting_logo_direction_reverse.set_active(direction == LightingDirection.BACKWARD)

    def set_logo_colors(self, lighting_colors: LightingColors) -> None:
        colors: List[LightingColor] = lighting_colors.colors
        if colors:
            for index, color in enumerate(colors):
                self._lighting_logo_button_list[index].set_rgba(LightingColor.to_button_color(color))
            self._lighting_logo_colors_spinbutton.set_value(len(colors))

    def set_ring_mode_id(self, mode_id: int) -> None:
        self._lighting_ring_mode_combobox.set_active_id(str(mode_id))

    def set_ring_speed_id(self, speed_id: int) -> None:
        self._lighting_ring_speed_combobox.set_active_id(str(speed_id))

    def set_ring_direction(self, direction: LightingDirection) -> None:
        self._lighting_ring_direction_reverse.set_active(direction == LightingDirection.BACKWARD)

    def set_ring_colors(self, lighting_colors: LightingColors) -> None:
        colors: List[LightingColor] = lighting_colors.colors
        if colors:
            for index, color in enumerate(colors):
                self._lighting_ring_button_list[index].set_rgba(LightingColor.to_button_color(color))
            self._lighting_ring_colors_spinbutton.set_value(len(colors))
