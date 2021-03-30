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

from gkraken.model.lighting_modes import LightingModes, LightingMode
from gkraken.model.lighting_settings import LightingColors, LightingDirection


class LightingViewInterface:

    def load_color_modes(self, lighting_modes: LightingModes) -> None:
        raise NotImplementedError()

    def set_statusbar_text(self, text: str) -> None:
        raise NotImplementedError()

    def set_lighting_apply_button_enabled(self, enabled: bool) -> None:
        raise NotImplementedError()

    def get_logo_mode_id(self) -> int:
        raise NotImplementedError()

    def set_lighting_logo_color_buttons_enabled(self, max_colors: int) -> None:
        raise NotImplementedError()

    def get_logo_colors(self, max_colors: int) -> LightingColors:
        raise NotImplementedError()

    def set_lighting_logo_spin_button(self, lighting_mode: LightingMode) -> None:
        raise NotImplementedError()

    def get_lighting_logo_spin_button(self) -> int:
        raise NotImplementedError()

    def set_lighting_logo_speed_enabled(self, enabled: bool) -> None:
        raise NotImplementedError()

    def get_lighting_logo_speed(self) -> int:
        raise NotImplementedError()

    def set_lighting_logo_direction_enabled(self, enabled: bool) -> None:
        raise NotImplementedError()

    def get_lighting_logo_direction(self) -> LightingDirection:
        raise NotImplementedError()

    def get_ring_mode_id(self) -> int:
        raise NotImplementedError()

    def set_lighting_ring_color_buttons_enabled(self, max_colors: int) -> None:
        raise NotImplementedError()

    def get_ring_colors(self, max_colors: int) -> LightingColors:
        raise NotImplementedError()

    def set_lighting_ring_spin_button(self, lighting_mode: LightingMode) -> None:
        raise NotImplementedError()

    def get_lighting_ring_spin_button(self) -> int:
        raise NotImplementedError()

    def set_lighting_ring_speed_enabled(self, enabled: bool) -> None:
        raise NotImplementedError()

    def get_lighting_ring_speed(self) -> int:
        raise NotImplementedError()

    def set_lighting_ring_direction_enabled(self, enabled: bool) -> None:
        raise NotImplementedError()

    def get_lighting_ring_direction(self) -> LightingDirection:
        raise NotImplementedError()
    
    def set_logo_mode_id(self, mode_id: int) -> None:
        raise NotImplementedError()

    def set_logo_speed_id(self, speed_id: int) -> None:
        raise NotImplementedError()

    def set_logo_direction(self, direction: LightingDirection) -> None:
        raise NotImplementedError()

    def set_logo_colors(self, colors: LightingColors) -> None:
        raise NotImplementedError()

    def set_ring_mode_id(self, mode_id: int) -> None:
        raise NotImplementedError()

    def set_ring_speed_id(self, speed_id: int) -> None:
        raise NotImplementedError()

    def set_ring_direction(self, direction: LightingDirection) -> None:
        raise NotImplementedError()

    def set_ring_colors(self, colors: LightingColors) -> None:
        raise NotImplementedError()
