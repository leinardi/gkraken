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

from typing import Optional, List, Tuple

from gkraken.model import ChannelType, SpeedProfile
from gkraken.model.status import Status


class MainViewInterface:

    def toggle_window_visibility(self) -> None:
        raise NotImplementedError()

    def refresh_status(self, status: Optional[Status]) -> None:
        raise NotImplementedError()

    def refresh_profile_combobox(self, channel: ChannelType, data: List[Tuple[int, str]],
                                 active: Optional[int]) -> None:
        raise NotImplementedError()

    def refresh_chart(self, profile: Optional[SpeedProfile] = None, channel_to_reset: Optional[str] = None) -> None:
        raise NotImplementedError()

    def set_apply_button_enabled(self, channel: ChannelType, enabled: bool) -> None:
        raise NotImplementedError()

    def set_edit_button_enabled(self, channel: ChannelType, enabled: bool) -> None:
        raise NotImplementedError()

    def set_statusbar_text(self, text: str) -> None:
        raise NotImplementedError()

    def show_main_infobar_message(self, message: str, markup: bool = False) -> None:
        raise NotImplementedError()

    def show_add_speed_profile_dialog(self, channel: ChannelType) -> None:
        raise NotImplementedError()

    def show_fixed_speed_profile_popover(self, profile: SpeedProfile) -> None:
        raise NotImplementedError()

    def dismiss_and_get_value_fixed_speed_popover(self) -> Tuple[int, str]:
        raise NotImplementedError()

    def show_about_dialog(self) -> None:
        raise NotImplementedError()

    def show_legacy_firmware_dialog(self) -> None:
        raise NotImplementedError()

    def show_error_message_dialog(self, title: str, message: str) -> None:
        raise NotImplementedError()
