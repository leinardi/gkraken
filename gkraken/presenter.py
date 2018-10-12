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
import multiprocessing
import re
from typing import Optional, Any, List, Tuple, Dict, Callable

from gi.repository import Gtk
from injector import inject, singleton
from rx import Observable
from rx.concurrency import GtkScheduler, ThreadPoolScheduler
from rx.concurrency.schedulerbase import SchedulerBase
from rx.disposables import CompositeDisposable

from gkraken.conf import SETTINGS_DEFAULTS
from gkraken.interactor import GetStatusInteractor, SetSpeedProfileInteractor, SettingsInteractor
from gkraken.model import Status, SpeedProfile, ChannelType, CurrentSpeedProfile, SpeedStep

LOG = logging.getLogger(__name__)
_ADD_NEW_PROFILE_INDEX = -10


class ViewInterface:
    def toggle_window_visibility(self) -> None:
        raise NotImplementedError()

    def refresh_status(self, status: Optional[Status]) -> None:
        raise NotImplementedError()

    def refresh_profile_combobox(self, channel: ChannelType, data: List[Tuple[int, str]],
                                 active: Optional[int]) -> None:
        raise NotImplementedError()

    def refresh_chart(self, profile: SpeedProfile) -> None:
        raise NotImplementedError()

    def set_apply_button_enabled(self, channel: ChannelType, enabled: bool) -> None:
        raise NotImplementedError()

    def set_edit_button_enabled(self, channel: ChannelType, enabled: bool) -> None:
        raise NotImplementedError()

    def set_statusbar_text(self, text: str) -> None:
        raise NotImplementedError()

    def refresh_content_header_bar_title(self) -> None:
        raise NotImplementedError()

    def refresh_settings(self, settings: Dict[str, Any]) -> None:
        raise NotImplementedError()

    def show_add_speed_profile_dialog(self, channel: ChannelType) -> None:
        raise NotImplementedError()

    def show_fixed_speed_profile_popover(self, profile: SpeedProfile) -> None:
        raise NotImplementedError()

    def dismiss_and_get_value_fixed_speed_popover(self) -> Tuple[int, str]:
        raise NotImplementedError()

    def show_settings_dialog(self) -> None:
        raise NotImplementedError()

    def hide_settings_dialog(self) -> None:
        raise NotImplementedError()


@singleton
class Presenter:
    @inject
    def __init__(self,
                 get_status_interactor: GetStatusInteractor,
                 set_speed_profile_interactor: SetSpeedProfileInteractor,
                 settings_interactor: SettingsInteractor,
                 composite_disposable: CompositeDisposable,
                 ) -> None:
        LOG.debug("init Presenter ")
        self.view: ViewInterface = ViewInterface()
        self.__scheduler: SchedulerBase = ThreadPoolScheduler(multiprocessing.cpu_count())
        self.__get_status_interactor: GetStatusInteractor = get_status_interactor
        self.__set_speed_profile_interactor: SetSpeedProfileInteractor = set_speed_profile_interactor
        self.__settings_interactor = settings_interactor
        self.__composite_disposable: CompositeDisposable = composite_disposable
        self.__profile_selected: Dict[str, SpeedProfile] = {}
        self.__should_update_fan_speed: bool = False
        self.application_quit: Callable = lambda *args: None  # will be set by the Application

    def on_start(self) -> None:
        self.__init_speed_profiles()
        self.__init_settings()
        self.__start_refresh()

    def __start_refresh(self) -> None:
        LOG.debug("start refresh")
        refresh_interval_ms = self.__settings_interactor.get_int('settings_refresh_interval') * 1000
        self.__composite_disposable \
            .add(Observable
                 .interval(refresh_interval_ms, scheduler=self.__scheduler)
                 .start_with(0)
                 .subscribe_on(self.__scheduler)
                 .flat_map(lambda _: self.__get_status())
                 .observe_on(GtkScheduler())
                 .subscribe(on_next=self.__update_status,
                            on_error=lambda e: LOG.exception("Refresh error: %s", str(e)))
                 )

    def __update_status(self, status: Optional[Status]) -> None:
        if status is not None:
            if self.__should_update_fan_speed:
                last_applied: CurrentSpeedProfile = CurrentSpeedProfile.get_or_none(channel=ChannelType.FAN.value)
                if last_applied is not None:
                    duties = [i.duty for i in last_applied.profile.steps if status.liquid_temperature >= i.temperature]
                    if duties:
                        status.fan_speed = duties[-1]

            self.view.refresh_status(status)

    # def __load_last_profile(self) -> None:
    #     for current in CurrentSpeedProfile.select():

    @staticmethod
    def __get_profile_list(channel: ChannelType) -> List[Tuple[int, str]]:
        return [(p.id, p.name) for p in SpeedProfile.select().where(SpeedProfile.channel == channel.value)]

    def __init_speed_profiles(self) -> None:
        for channel in ChannelType:
            data = self.__get_profile_list(channel)

            active = None
            if self.__settings_interactor.get_bool('settings_load_last_profile'):
                self.__should_update_fan_speed = True
                current: CurrentSpeedProfile = CurrentSpeedProfile.get_or_none(channel=channel.value)
                if current is not None:
                    active = next(i for i, item in enumerate(data) if item[0] == current.profile.id)
                    self.__set_speed_profile(current.profile)

            data.append((_ADD_NEW_PROFILE_INDEX, "<span style='italic' alpha='50%'>Add new profile...</span>"))

            self.view.refresh_profile_combobox(channel, data, active)

    def __init_settings(self) -> None:
        settings: Dict[str, Any] = {}
        for key, default_value in SETTINGS_DEFAULTS.items():
            if isinstance(default_value, bool):
                settings[key] = self.__settings_interactor.get_bool(key)
            elif isinstance(default_value, int):
                settings[key] = self.__settings_interactor.get_int(key)
        self.view.refresh_settings(settings)

    def on_menu_settings_clicked(self, *_: Any) -> None:
        self.view.show_settings_dialog()

    def on_settings_dialog_closed(self, *_: Any) -> bool:
        self.view.hide_settings_dialog()
        return True

    def on_setting_changed(self, widget: Any, *args: Any) -> None:
        key = value = None
        if isinstance(widget, Gtk.Switch):
            value = args[0]
            key = re.sub('_switch$', '', widget.get_name())
        elif isinstance(widget, Gtk.SpinButton):
            key = re.sub('_spinbutton$', '', widget.get_name())
            value = widget.get_value_as_int()
        if key is not None and value is not None:
            self.__settings_interactor.set_bool(key, value)

    def on_stack_visible_child_changed(self, *_: Any) -> None:
        self.view.refresh_content_header_bar_title()

    def on_fan_profile_selected(self, widget: Any, *_: Any) -> None:
        profile_id = widget.get_model()[widget.get_active()][0]
        self.__select_speed_profile(profile_id, ChannelType.FAN)

    def on_pump_profile_selected(self, widget: Any, *_: Any) -> None:
        profile_id = widget.get_model()[widget.get_active()][0]
        self.__select_speed_profile(profile_id, ChannelType.PUMP)

    def on_quit_clicked(self, *_: Any) -> None:
        self.application_quit()

    def on_toggle_app_window_clicked(self, *_: Any) -> None:
        self.view.toggle_window_visibility()

    def __select_speed_profile(self, profile_id: int, channel: ChannelType) -> None:
        if profile_id == _ADD_NEW_PROFILE_INDEX:
            self.view.set_apply_button_enabled(channel, False)
            self.view.set_edit_button_enabled(channel, False)
            self.view.show_add_speed_profile_dialog(channel)
        else:
            profile: SpeedProfile = SpeedProfile.get(id=profile_id)
            self.__profile_selected[profile.channel] = profile
            self.view.set_apply_button_enabled(channel, True)
            self.view.set_edit_button_enabled(channel, True)
            self.view.refresh_chart(profile)

    @staticmethod
    def __get_profile_data(profile: SpeedProfile) -> List[Tuple[int, int]]:
        return [(p.temperature, p.duty) for p in profile.steps]

    def on_fan_edit_button_clicked(self, *_: Any) -> None:
        self.__on_edit_button_clicked(ChannelType.FAN)

    def on_pump_edit_button_clicked(self, *_: Any) -> None:
        self.__on_edit_button_clicked(ChannelType.PUMP)

    def __on_edit_button_clicked(self, channel: ChannelType) -> None:
        profile = self.__profile_selected[channel.value]
        if profile.single_step:
            self.view.show_fixed_speed_profile_popover(profile)

    def on_fixed_speed_apply_button_clicked(self, *_: Any) -> None:
        value, channel = self.view.dismiss_and_get_value_fixed_speed_popover()
        profile = self.__profile_selected[channel]
        speed_step: SpeedStep = profile.steps[0]
        speed_step.duty = value
        speed_step.save()
        if channel == ChannelType.FAN.value:
            self.__should_update_fan_speed = False
        self.view.refresh_chart(profile)

    def on_fan_apply_button_clicked(self, *_: Any) -> None:
        self.__set_speed_profile(self.__profile_selected[ChannelType.FAN.value])
        self.__should_update_fan_speed = True

    def on_pump_apply_button_clicked(self, *_: Any) -> None:
        self.__set_speed_profile(self.__profile_selected[ChannelType.PUMP.value])

    def __set_speed_profile(self, profile: SpeedProfile) -> None:
        observable = self.__set_speed_profile_interactor \
            .execute(profile.channel, self.__get_profile_data(profile))
        self.__composite_disposable \
            .add(observable
                 .subscribe_on(self.__scheduler)
                 .observe_on(GtkScheduler())
                 .subscribe(on_next=lambda _: self.__update_current_speed_profile(profile),
                            on_error=lambda e: (LOG.exception("Set cooling error: %s", str(e)),
                                                self.view.set_statusbar_text('Error applying %s speed profile!'
                                                                             % profile.channel))))

    def __update_current_speed_profile(self, profile: SpeedProfile) -> None:
        current: CurrentSpeedProfile = CurrentSpeedProfile.get_or_none(channel=profile.channel)
        if current is None:
            CurrentSpeedProfile.create(channel=profile.channel, profile=profile)
        else:
            current.profile = profile
            current.save()
        self.view.set_statusbar_text('%s cooling profile applied' % profile.channel.capitalize())

    def __log_exception_return_empty_observable(self, ex: Exception) -> Observable:
        LOG.exception("Err = %s", ex)
        self.view.set_statusbar_text(str(ex))
        return Observable.just(None)

    def __get_status(self) -> Observable:
        return self.__get_status_interactor.execute() \
            .catch_exception(self.__log_exception_return_empty_observable)
