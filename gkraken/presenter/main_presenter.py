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
from typing import Optional, Any, List, Tuple, Dict, Callable

import rx
from gi.repository import GLib
from injector import inject, singleton
from rx import Observable, operators
from rx.disposable import CompositeDisposable
from rx.scheduler.mainloop import GtkScheduler

from gkraken.conf import APP_PACKAGE_NAME, APP_NAME, APP_SOURCE_URL, APP_VERSION, APP_ID, APP_SUPPORTED_MODELS
from gkraken.di import SpeedProfileChangedSubject, SpeedStepChangedSubject
from gkraken.interactor.check_new_version_interactor import CheckNewVersionInteractor
from gkraken.interactor.get_status_interactor import GetStatusInteractor
from gkraken.interactor.has_supported_kraken_interactor import HasSupportedKrakenInteractor
from gkraken.interactor.set_speed_profile_interactor import SetSpeedProfileInteractor
from gkraken.interactor.settings_interactor import SettingsInteractor
from gkraken.model.status import Status
from gkraken.model.speed_profile import SpeedProfile
from gkraken.model.channel_type import ChannelType
from gkraken.model.current_speed_profile import CurrentSpeedProfile
from gkraken.model.speed_step import SpeedStep
from gkraken.model.db_change import DbChange
from gkraken.presenter.edit_speed_profile_presenter import EditSpeedProfilePresenter
from gkraken.presenter.lighting_presenter import LightingPresenter
from gkraken.presenter.preferences_presenter import PreferencesPresenter
from gkraken.presenter.scheduler import Scheduler
from gkraken.util.deployment import is_flatpak
from gkraken.util.view import open_uri, get_default_application
from gkraken.view.main_view_interface import MainViewInterface

_LOG = logging.getLogger(__name__)
_ADD_NEW_PROFILE_INDEX = -10


@singleton
class MainPresenter:
    @inject
    def __init__(self,
                 edit_speed_profile_presenter: EditSpeedProfilePresenter,
                 preferences_presenter: PreferencesPresenter,
                 lighting_presenter: LightingPresenter,
                 has_supported_kraken_interactor: HasSupportedKrakenInteractor,
                 get_status_interactor: GetStatusInteractor,
                 set_speed_profile_interactor: SetSpeedProfileInteractor,
                 settings_interactor: SettingsInteractor,
                 check_new_version_interactor: CheckNewVersionInteractor,
                 speed_profile_changed_subject: SpeedProfileChangedSubject,
                 speed_step_changed_subject: SpeedStepChangedSubject,
                 composite_disposable: CompositeDisposable,
                 scheduler: Scheduler,
                 ) -> None:
        _LOG.debug("init MainPresenter ")
        self.main_view: MainViewInterface = MainViewInterface()
        self._edit_speed_profile_presenter = edit_speed_profile_presenter
        self._preferences_presenter = preferences_presenter
        self._lighting_presenter: LightingPresenter = lighting_presenter
        self._scheduler = scheduler.get()
        self._has_supported_kraken_interactor = has_supported_kraken_interactor
        self._get_status_interactor: GetStatusInteractor = get_status_interactor
        self._set_speed_profile_interactor: SetSpeedProfileInteractor = set_speed_profile_interactor
        self._settings_interactor = settings_interactor
        self._check_new_version_interactor = check_new_version_interactor
        self._speed_profile_changed_subject = speed_profile_changed_subject
        self._speed_step_changed_subject = speed_step_changed_subject
        self._composite_disposable: CompositeDisposable = composite_disposable
        self._profile_selected: Dict[str, SpeedProfile] = {}
        self._should_update_fan_speed: bool = False
        self._should_update_pump_speed: bool = False
        self._legacy_firmware_dialog_shown: bool = False
        self.application_quit: Callable = lambda *args: None  # will be set by the Application
        self._critical_error_occurred: bool = False  # to handle multiple startup errors

    def on_start(self) -> None:
        self._register_db_listeners()
        self._check_supported_kraken()
        self._load_lighting_modes()
        self._refresh_speed_profiles(True)
        if self._settings_interactor.get_int('settings_check_new_version'):
            self._check_new_version()

    def on_application_window_delete_event(self, *_: Any) -> bool:
        if self._settings_interactor.get_int('settings_minimize_to_tray'):
            self.on_toggle_app_window_clicked()
            return True
        return False

    def _register_db_listeners(self) -> None:
        self._speed_profile_changed_subject.subscribe(on_next=self._on_speed_profile_list_changed,
                                                      on_error=lambda e: _LOG.exception("Db signal error: %s", str(e)))
        self._speed_step_changed_subject.subscribe(on_next=self._on_speed_step_list_changed,
                                                   on_error=lambda e: _LOG.exception("Db signal error: %s", str(e)))

    def _on_speed_profile_list_changed(self, db_change: DbChange) -> None:
        profile = db_change.entry
        if db_change.type == DbChange.DELETE:
            self._refresh_speed_profile(ChannelType(profile.channel))
            self._profile_selected.pop(profile.channel, None)
        elif db_change.type == DbChange.INSERT or db_change.type == DbChange.UPDATE:
            self._refresh_speed_profile(ChannelType(profile.channel), profile_id=profile.id)

    def _on_speed_step_list_changed(self, db_change: DbChange) -> None:
        profile = db_change.entry.profile
        if profile.channel in self._profile_selected and self._profile_selected[profile.channel].id == profile.id:
            self.main_view.refresh_chart(profile)

    def _check_supported_kraken(self) -> None:
        self._composite_disposable.add(self._has_supported_kraken_interactor.execute().pipe(
            operators.subscribe_on(self._scheduler),
            operators.observe_on(GtkScheduler(GLib)),
        ).subscribe(on_next=self._has_supported_kraken_result))

    def _has_supported_kraken_result(self, has_supported_kraken: bool) -> None:
        if has_supported_kraken:
            self._start_refresh()
        else:
            _LOG.error("Unable to find supported Kraken device!")
            self.main_view.show_error_message_dialog(
                "Unable to find supported NZXT Kraken devices",
                "It was not possible to connect to any of the supported NZXT Kraken devices.\n\n"
                f"{APP_NAME} currently supports only {APP_SUPPORTED_MODELS}.\n\n"
                "If one of the supported devices is connected, try to run the following command and then reboot:\n\n"
                f"{self._get_udev_command()}"
            )
            get_default_application().quit()

    def _start_refresh(self) -> None:
        _LOG.debug("start refresh")
        refresh_interval = self._settings_interactor.get_int('settings_refresh_interval')
        self._composite_disposable.add(rx.interval(refresh_interval, scheduler=self._scheduler).pipe(
            operators.start_with(0),
            operators.subscribe_on(self._scheduler),
            operators.flat_map(lambda _: self._get_status()),
            operators.observe_on(GtkScheduler(GLib)),
        ).subscribe(on_next=self._update_status,
                    on_error=self._handle_refresh_error))

    def _handle_refresh_error(self, ex: Exception) -> None:
        if isinstance(ex, OSError):
            if not self._critical_error_occurred:
                self._critical_error_occurred = True
                self.main_view.show_error_message_dialog(
                    "Unable to communicate with the NZXT Kraken",
                    "It was not possible to communicate with the NZXT Kraken.\n\n"
                    "Most probably the current user does not have the permission to access it.\n\n"
                    "You can try to fix the issue running the following command and then rebooting:\n\n"
                    f"{self._get_udev_command()}\n\n"
                    "For more info check the section \"Adding Udev rule\" of the project's README.md.")
                get_default_application().quit()
        _LOG.exception("Refresh error: %s", str(ex))

    @staticmethod
    def _get_udev_command() -> str:
        command = APP_PACKAGE_NAME
        if is_flatpak():
            command = f"flatpak run {APP_ID}"
        command += " --add-udev-rule"
        return command

    def _update_status(self, status: Optional[Status]) -> Optional[Status]:
        if status is not None:
            if self._should_update_fan_speed:
                last_applied_fan_profile: CurrentSpeedProfile = CurrentSpeedProfile.get_or_none(
                    channel=ChannelType.FAN.value)
                if last_applied_fan_profile is not None and status.fan_duty is None and status.fan_rpm is not None:
                    _LOG.debug("No Fan Duty reported from device, calculating based on speed profile")
                    status.fan_duty = self._calculate_duty(last_applied_fan_profile.profile, status.liquid_temperature)
            if self._should_update_pump_speed:
                last_applied_pump_profile: CurrentSpeedProfile = CurrentSpeedProfile.get_or_none(
                    channel=ChannelType.PUMP.value)
                if last_applied_pump_profile is not None and status.pump_duty is None and status.pump_rpm is not None:
                    _LOG.debug("No Pump Duty reported from device, calculating based on speed profile")
                    status.pump_duty = self._calculate_duty(last_applied_pump_profile.profile,
                                                            status.liquid_temperature)
            self.main_view.refresh_status(status)
            if not self._legacy_firmware_dialog_shown and status.firmware_version.startswith('2.'):
                self._legacy_firmware_dialog_shown = True
                self.main_view.show_legacy_firmware_dialog()
        return status

    @staticmethod
    def _calculate_duty(profile: SpeedProfile, liquid_temperature: float) -> float:
        p_1 = ([(i.temperature, i.duty) for i in profile.steps if i.temperature <= liquid_temperature] or [None])[-1]
        p_2 = next(((i.temperature, i.duty) for i in profile.steps if i.temperature > liquid_temperature), None)
        duty = 0.0
        if p_1 and p_2:
            duty = ((p_2[1] - p_1[1]) / (p_2[0] - p_1[0])) * (liquid_temperature - p_1[0]) + p_1[1]
        elif p_1:
            duty = float(p_1[1])
        elif p_2:
            duty = float(p_2[1])
        return duty

    @staticmethod
    def _get_profile_list(channel: ChannelType) -> List[Tuple[int, str]]:
        return [(p.id, p.name) for p in SpeedProfile.select().where(SpeedProfile.channel == channel.value)]

    def _refresh_speed_profiles(self, init: bool = False, selecter_profile_id: Optional[int] = None) -> None:
        self._get_status().pipe(
            operators.map(self._update_status),
            operators.flat_map(lambda status: rx.from_list(
                [channel for channel in ChannelType]
            ).pipe(
                operators.filter(lambda channel: self._is_channel_supported(channel, status))
            ))
        ).subscribe(
            on_next=lambda channel: self._refresh_speed_profile(channel, init, selecter_profile_id),
            on_error=self._handle_refresh_error
        )

    @staticmethod
    def _is_channel_supported(channel: ChannelType, status: Status) -> bool:
        return {
            ChannelType.FAN: status.fan_rpm is not None,
            ChannelType.PUMP: status.pump_rpm is not None
        }.get(channel, True)

    def _refresh_speed_profile(self, channel: ChannelType, init: bool = False,
                               profile_id: Optional[int] = None) -> None:
        data = self._get_profile_list(channel)
        active = None
        if profile_id is not None:
            active = next(i for i, item in enumerate(data) if item[0] == profile_id)
        elif init and self._settings_interactor.get_bool('settings_load_last_profile'):
            self._should_update_fan_speed = True
            self._should_update_pump_speed = True
            current: CurrentSpeedProfile = CurrentSpeedProfile.get_or_none(channel=channel.value)
            if current is not None:
                active = next(i for i, item in enumerate(data) if item[0] == current.profile.id)
                self._set_speed_profile(current.profile)
        data.append((_ADD_NEW_PROFILE_INDEX, "<span style='italic' alpha='50%'>Add new profile...</span>"))
        self.main_view.refresh_profile_combobox(channel, data, active)

    def on_menu_settings_clicked(self, *_: Any) -> None:
        self._preferences_presenter.show()

    def on_menu_changelog_clicked(self, *_: Any) -> None:
        open_uri(self._get_changelog_uri())

    def on_menu_about_clicked(self, *_: Any) -> None:
        self.main_view.show_about_dialog()

    def on_stack_visible_child_changed(self, *_: Any) -> None:
        pass

    def on_fan_profile_selected(self, widget: Any, *_: Any) -> None:
        active = widget.get_active()
        if active >= 0:
            profile_id = widget.get_model()[active][0]
            self._select_speed_profile(profile_id, ChannelType.FAN)

    def on_pump_profile_selected(self, widget: Any, *_: Any) -> None:
        active = widget.get_active()
        if active >= 0:
            profile_id = widget.get_model()[active][0]
            self._select_speed_profile(profile_id, ChannelType.PUMP)

    def on_quit_clicked(self, *_: Any) -> None:
        self.application_quit()

    def on_toggle_app_window_clicked(self, *_: Any) -> None:
        self.main_view.toggle_window_visibility()

    def _select_speed_profile(self, profile_id: int, channel: ChannelType) -> None:
        if profile_id == _ADD_NEW_PROFILE_INDEX:
            self.main_view.set_apply_button_enabled(channel, False)
            self.main_view.set_edit_button_enabled(channel, False)
            self.main_view.show_add_speed_profile_dialog(channel)
            self.main_view.refresh_chart(channel_to_reset=channel.value)
            self._edit_speed_profile_presenter.show_add(channel)
        else:
            profile: SpeedProfile = SpeedProfile.get(id=profile_id)
            self._profile_selected[profile.channel] = profile
            if profile.read_only:
                self.main_view.set_edit_button_enabled(channel, False)
            else:
                self.main_view.set_edit_button_enabled(channel, True)
            self.main_view.set_apply_button_enabled(channel, True)
            self.main_view.refresh_chart(profile)

    @staticmethod
    def _get_profile_data(profile: SpeedProfile) -> List[Tuple[int, int]]:
        return [(p.temperature, p.duty) for p in profile.steps]

    def on_fan_edit_button_clicked(self, *_: Any) -> None:
        self._on_edit_button_clicked(ChannelType.FAN)

    def on_pump_edit_button_clicked(self, *_: Any) -> None:
        self._on_edit_button_clicked(ChannelType.PUMP)

    def _on_edit_button_clicked(self, channel: ChannelType) -> None:
        profile = self._profile_selected[channel.value]
        if profile.single_step:
            self.main_view.show_fixed_speed_profile_popover(profile)
        else:
            self._edit_speed_profile_presenter.show_edit(profile)

    def on_fixed_speed_apply_button_clicked(self, *_: Any) -> None:
        value, channel = self.main_view.dismiss_and_get_value_fixed_speed_popover()
        profile = self._profile_selected[channel]
        speed_step: SpeedStep = profile.steps[0]
        speed_step.duty = value
        speed_step.save()
        if channel == ChannelType.FAN.value:
            self._should_update_fan_speed = False
        elif channel == ChannelType.PUMP.value:
            self._should_update_pump_speed = False
        self.main_view.refresh_chart(profile)

    def on_fan_apply_button_clicked(self, *_: Any) -> None:
        channel = ChannelType.FAN.value
        self.main_view.set_statusbar_text('applying %s cooling profile...' % channel)
        self._set_speed_profile(self._profile_selected[channel])
        self._should_update_fan_speed = True

    def on_pump_apply_button_clicked(self, *_: Any) -> None:
        channel = ChannelType.PUMP.value
        self.main_view.set_statusbar_text('applying %s cooling profile...' % channel)
        self._set_speed_profile(self._profile_selected[channel])
        self._should_update_pump_speed = True

    def _set_speed_profile(self, profile: SpeedProfile) -> None:
        observable = self._set_speed_profile_interactor \
            .execute(profile.channel, self._get_profile_data(profile))
        self._composite_disposable.add(observable.pipe(
            operators.subscribe_on(self._scheduler),
            operators.observe_on(GtkScheduler(GLib)),
        ).subscribe(on_next=lambda _: self._update_current_speed_profile(profile),
                    on_error=lambda e: self._on_set_speed_profile_error(e, profile)))

    def _on_set_speed_profile_error(self, e: Exception, profile: SpeedProfile) -> None:
        _LOG.exception("Set cooling error: %s", str(e))
        self.main_view.set_statusbar_text('Error applying %s speed profile!' % profile.channel)

    def _update_current_speed_profile(self, profile: SpeedProfile) -> None:
        current: CurrentSpeedProfile = CurrentSpeedProfile.get_or_none(channel=profile.channel)
        if current is None:
            CurrentSpeedProfile.create(channel=profile.channel, profile=profile)
        else:
            current.profile = profile
            current.save()
        self.main_view.set_statusbar_text('%s cooling profile applied' % profile.channel.capitalize())

    def _log_exception_return_empty_observable(self, ex: Exception, _: Observable) -> Observable:
        _LOG.exception("Err = %s", ex)
        self.main_view.set_statusbar_text(str(ex))
        if isinstance(ex, OSError):
            raise ex
        observable = rx.just(None)
        assert isinstance(operators, Observable)
        return observable

    def _get_status(self) -> Observable:
        observable = self._get_status_interactor.execute().pipe(
            operators.catch(self._log_exception_return_empty_observable),
            operators.map(self.log_status)
        )

        assert isinstance(observable, Observable)
        return observable

    @staticmethod
    def log_status(status: Status) -> Status:
        _LOG.debug("Internal Status is: %s", repr(status))
        return status

    def _check_new_version(self) -> None:
        self._composite_disposable.add(self._check_new_version_interactor.execute().pipe(
            operators.subscribe_on(self._scheduler),
            operators.observe_on(GtkScheduler(GLib)),
        ).subscribe(on_next=self._handle_new_version_response,
                    on_error=lambda e: _LOG.exception("Check new version error: %s", str(e))))

    def _handle_new_version_response(self, version: Optional[str]) -> None:
        if version is not None:
            message = "%s version <b>%s</b> is available! Click <a href=\"%s/blob/%s/CHANGELOG.md\"><b>here</b></a> " \
                      "to see what's new." % (APP_NAME, version, APP_SOURCE_URL, version)
            self.main_view.show_main_infobar_message(message, True)

    @staticmethod
    def _get_changelog_uri(version: str = APP_VERSION) -> str:
        return f"{APP_SOURCE_URL}/blob/{version}/CHANGELOG.md"

    def _load_lighting_modes(self) -> None:
        self._lighting_presenter.load_lighting_modes()

    def on_logo_mode_selected(self, *_: Any) -> None:
        self._lighting_presenter.on_logo_mode_selected()

    def on_ring_mode_selected(self, *_: Any) -> None:
        self._lighting_presenter.on_ring_mode_selected()

    def on_lighting_logo_colors_spinbutton_changed(self, spinbutton: Any) -> None:
        self._lighting_presenter.on_lighting_logo_colors_spinbutton_changed(spinbutton)

    def on_lighting_ring_colors_spinbutton_changed(self, spinbutton: Any) -> None:
        self._lighting_presenter.on_lighting_ring_colors_spinbutton_changed(spinbutton)

    def on_lighting_apply_button_clicked(self, *_: Any) -> None:
        self._lighting_presenter.on_lighting_apply_button_clicked()
