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
from typing import Optional, Any, List, Tuple

from injector import inject, singleton
from rx import Observable
from rx.concurrency import GtkScheduler, ThreadPoolScheduler
from rx.concurrency.schedulerbase import SchedulerBase
from rx.disposables import CompositeDisposable

from gkraken.interactor import GetStatusInteractor, SetSpeedProfileInteractor, SettingsInteractor
from gkraken.model import Status, SpeedProfile, ChannelType

LOG = logging.getLogger(__name__)
_REFRESH_INTERVAL_IN_MS = 3000
_ADD_NEW_PROFILE_INDEX = -10


class ViewInterface:
    def refresh_status(self, status: Optional[Status]) -> None:
        raise NotImplementedError()

    def refresh_fan_profile_combobox(self, data: List[Tuple[int, str]]) -> None:
        raise NotImplementedError()

    def refresh_pump_profile_combobox(self, data: List[Tuple[int, str]]) -> None:
        raise NotImplementedError()

    def refresh_fan_chart(self, profile: SpeedProfile) -> None:
        raise NotImplementedError()

    def refresh_pump_chart(self, profile: SpeedProfile) -> None:
        raise NotImplementedError()

    def set_apply_button_enabled(self, channel: ChannelType, enabled: bool) -> None:
        raise NotImplementedError()

    def set_statusbar_text(self, text: str) -> None:
        raise NotImplementedError()

    def refresh_content_header_bar_title(self) -> None:
        raise NotImplementedError()

    def show_add_speed_profile_dialog(self, channel: ChannelType) -> None:
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
        self.__fan_profile_selected: Optional[SpeedProfile] = None
        self.__pump_profile_selected: Optional[SpeedProfile] = None

    def on_start(self) -> None:
        self.__refresh_speed_profiles()
        self.__start_refresh()

    def __start_refresh(self) -> None:
        LOG.debug("start refresh")
        self.__composite_disposable \
            .add(Observable
                 .interval(_REFRESH_INTERVAL_IN_MS, scheduler=self.__scheduler)
                 .start_with(0)
                 .subscribe_on(self.__scheduler)
                 .flat_map(lambda _: self.__get_status())
                 .observe_on(GtkScheduler())
                 .subscribe(on_next=self.view.refresh_status,
                            on_error=lambda e: LOG.exception("Refresh error: %s", str(e)))
                 )

    @staticmethod
    def __get_profile_list(channel: ChannelType) -> List[Tuple[int, str]]:
        return [(p.id, p.name) for p in SpeedProfile.select().where(SpeedProfile.channel == channel.value)]

    def __refresh_speed_profiles(self) -> None:
        data = self.__get_profile_list(ChannelType.FAN)
        data.append((_ADD_NEW_PROFILE_INDEX, "<span style='italic' alpha='50%'>Add new profile...</span>"))
        self.view.refresh_fan_profile_combobox(data)

        data = self.__get_profile_list(ChannelType.PUMP)
        data.append((_ADD_NEW_PROFILE_INDEX, "<span style='italic' alpha='50%'>Add new profile...</span>"))
        self.view.refresh_pump_profile_combobox(data)

    def on_menu_settings_clicked(self, *_: Any) -> None:
        self.view.show_settings_dialog()

    def on_close_settings_dialog_button_clicked(self, *_: Any) -> None:
        self.view.hide_settings_dialog()

    def on_stack_visible_child_changed(self, *_: Any) -> None:
        self.view.refresh_content_header_bar_title()

    def on_fan_profile_selected(self, widget: Any, *_: Any) -> None:
        profile_id = widget.get_model()[widget.get_active()][0]
        if profile_id == _ADD_NEW_PROFILE_INDEX:
            self.view.set_apply_button_enabled(ChannelType.FAN, False)
            self.view.show_add_speed_profile_dialog(ChannelType.FAN)
        else:
            self.__fan_profile_selected = SpeedProfile.get(id=profile_id)
            self.view.set_apply_button_enabled(ChannelType.FAN, True)
            self.view.refresh_fan_chart(self.__fan_profile_selected)

    def on_pump_profile_selected(self, widget: Any, *_: Any) -> None:
        profile_id = widget.get_model()[widget.get_active()][0]
        if profile_id == _ADD_NEW_PROFILE_INDEX:
            self.view.set_apply_button_enabled(ChannelType.PUMP, False)
            self.view.show_add_speed_profile_dialog(ChannelType.PUMP)
        else:
            self.__pump_profile_selected = SpeedProfile.get(id=profile_id)
            self.view.set_apply_button_enabled(ChannelType.PUMP, True)
            self.view.refresh_pump_chart(self.__pump_profile_selected)

    @staticmethod
    def __get_profile_data(profile: SpeedProfile) -> List[Tuple[int, int]]:
        return [(p.temperature, p.duty) for p in profile.steps]

    def on_fab_apply_button_clicked(self, *_: Any) -> None:
        observable = self.__set_speed_profile_interactor \
            .execute(ChannelType.FAN.value, self.__get_profile_data(self.__fan_profile_selected))
        self.__set_speed(observable)

    def on_pump_apply_button_clicked(self, *_: Any) -> None:
        observable = self.__set_speed_profile_interactor \
            .execute(ChannelType.PUMP.value, self.__get_profile_data(self.__pump_profile_selected))
        self.__set_speed(observable)

    # @staticmethod
    # def __log_exception_return_system_info_observable(ex: Exception) -> Observable:
    #     LOG.exception("Err = %s", ex)
    #     return Observable.just(system_info)

    def __set_speed(self, observable: Observable) -> None:
        self.__composite_disposable \
            .add(observable
                 .subscribe_on(self.__scheduler)
                 .observe_on(GtkScheduler())
                 .subscribe(on_next=lambda _: self.view.set_statusbar_text('Cooling profile applied'),
                            on_error=lambda e: (LOG.exception("Set cooling error: %s", str(e)),
                                                self.view.set_statusbar_text('Error applying speed profile!'))))

    def __get_status(self) -> Observable:
        return self.__get_status_interactor.execute()  # \
        # .catch_exception(lambda ex: self.__log_exception_return_system_info_observable(system_info, ex))
