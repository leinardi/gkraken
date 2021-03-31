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
from typing import Any, Optional, List, Tuple

from gi.repository import GLib
from injector import singleton, inject
from rx import Observable, operators
from rx.disposable import CompositeDisposable
from rx.scheduler.mainloop import GtkScheduler

from gkraken.interactor.get_lighting_modes_interactor import GetLightingModesInteractor
from gkraken.interactor.set_lighting_interactor import SetLightingInteractor
from gkraken.interactor.settings_interactor import SettingsInteractor
from gkraken.model.current_lighting_color import CurrentLightingColor
from gkraken.model.current_lighting_profile import CurrentLightingProfile
from gkraken.model.lighting_modes import LightingModes
from gkraken.model.lighting_settings import LightingColors, LightingSettings, LightingColor, LightingChannel, \
    LightingDirection
from gkraken.model.lighting_speeds import LightingSpeeds
from gkraken.presenter.scheduler import Scheduler
from gkraken.view.lighting_view_interface import LightingViewInterface

_LOG = logging.getLogger(__name__)


@singleton
class LightingPresenter:
    @inject
    def __init__(self,
                 set_lighting_interactor: SetLightingInteractor,
                 get_lighting_modes_interactor: GetLightingModesInteractor,
                 settings_interactor: SettingsInteractor,
                 composite_disposable: CompositeDisposable,
                 scheduler: Scheduler,
                 ) -> None:
        _LOG.debug("init LightingPresenter ")
        self.view: LightingViewInterface = LightingViewInterface()
        self._set_lighting_interactor = set_lighting_interactor
        self._get_lighting_modes_interactor = get_lighting_modes_interactor
        self._settings_interactor = settings_interactor
        self._composite_disposable: CompositeDisposable = composite_disposable
        self._scheduler = scheduler.get()

    def load_lighting_modes(self) -> None:
        self._composite_disposable.add(
            self._get_lighting_modes().subscribe(
                on_next=self._initialize_lighting_modes,
                on_error=lambda e: _LOG.exception("Lighting error: %s", str(e))))

    def _initialize_lighting_modes(self, lighting_modes: LightingModes) -> None:
        self.view.load_color_modes(lighting_modes)
        self._load_current_lighting_modes()

    def _get_lighting_modes(self) -> Observable:
        return self._get_lighting_modes_interactor.execute(
        ).pipe(
            operators.subscribe_on(self._scheduler),
            operators.observe_on(GtkScheduler(GLib)),
        )

    def _load_current_lighting_modes(self) -> None:
        if self._settings_interactor.get_bool('settings_load_last_profile'):
            logo_profile, logo_colors = self._get_current_lighting_profiles(LightingChannel.LOGO)
            if logo_profile:
                _LOG.info("Saved Lighting Logo Profile found: %s, mode: %s, speed: %s, direction: %s, with %s colors",
                          logo_profile, logo_profile.mode, logo_profile.speed, logo_profile.direction,
                          len(logo_colors))
                self._set_lighting_logo_widgets(logo_profile, logo_colors)

            ring_profile, ring_colors = self._get_current_lighting_profiles(LightingChannel.RING)
            if ring_profile:
                _LOG.info("Savend Lighting Ring Profile found: %s, mode: %s, speed: %s, direction: %s, with %s colors",
                          ring_profile, ring_profile.mode, ring_profile.speed, ring_profile.direction,
                          len(ring_colors))
                self._set_lighting_ring_widgets(ring_profile, ring_colors)
            if logo_profile or ring_profile:
                self.on_lighting_apply_button_clicked()

    @staticmethod
    def _get_current_lighting_profiles(channel: LightingChannel
                                       ) -> Tuple[Optional[CurrentLightingProfile], List[CurrentLightingColor]]:
        profile: Optional[CurrentLightingProfile] = CurrentLightingProfile.get_or_none(
            channel=channel.value
        )

        current_colors: List[CurrentLightingColor] = CurrentLightingColor.select(
        ).where(
            CurrentLightingColor.channel == channel.value
        ).order_by(
            CurrentLightingColor.index
        )
        colors: List[CurrentLightingColor] = [color for color in current_colors]
        return profile, colors

    def _set_lighting_logo_widgets(self,
                                   logo_profile: CurrentLightingProfile,
                                   logo_colors: List[CurrentLightingColor]
                                   ) -> None:
        colors: LightingColors = self._convert_current_colors_to_lighting_colors(logo_colors)

        self.view.set_logo_mode_id(logo_profile.mode)
        self.view.set_logo_speed_id(logo_profile.speed)
        self.view.set_logo_direction(LightingDirection.from_str(logo_profile.direction))
        self.view.set_logo_colors(colors)

    def _set_lighting_ring_widgets(self,
                                   ring_profile: CurrentLightingProfile,
                                   ring_colors: List[CurrentLightingColor]
                                   ) -> None:
        colors: LightingColors = self._convert_current_colors_to_lighting_colors(ring_colors)

        self.view.set_ring_mode_id(ring_profile.mode)
        self.view.set_ring_speed_id(ring_profile.speed)
        self.view.set_ring_direction(LightingDirection.from_str(ring_profile.direction))
        self.view.set_ring_colors(colors)

    @staticmethod
    def _convert_current_colors_to_lighting_colors(current_colors: List[CurrentLightingColor]
                                                   ) -> LightingColors:
        lighting_colors = LightingColors()
        for current_color in current_colors:
            lighting_colors.add(
                LightingColor(current_color.red, current_color.green, current_color.blue))
        return lighting_colors

    def on_logo_mode_selected(self, *_: Any) -> None:
        mode_id = self.view.get_logo_mode_id()
        if mode_id > 0:
            self._get_lighting_modes(
            ).subscribe(
                on_next=lambda lighting_modes: self._update_logo_widgets(mode_id, lighting_modes),
                on_error=lambda e: _LOG.exception("Lighting error: %s", str(e))
            )
        else:
            raise IndexError("Logo Mode ID from the ListStore is unreadable")

    def _update_logo_widgets(self, mode_id: int, lighting_modes: LightingModes) -> None:
        chosen_logo_mode = lighting_modes.modes_logo[mode_id]
        self.view.set_lighting_logo_spin_button(chosen_logo_mode)
        self.view.set_lighting_logo_color_buttons_enabled(chosen_logo_mode.min_colors)
        self.view.set_lighting_logo_speed_enabled(chosen_logo_mode.speed_enabled)
        self.view.set_lighting_logo_direction_enabled(chosen_logo_mode.direction_enabled)
        self.view.set_lighting_apply_button_enabled(True)

    def on_lighting_apply_button_clicked(self, *_: Any) -> None:
        self.view.set_statusbar_text('applying Lighting...')
        self._get_lighting_modes(
        ).subscribe(
            on_next=self._set_lighting,
            on_error=self._on_lighting_apply_error
        )

    def _on_lighting_apply_error(self, e: Exception) -> None:
        _LOG.exception("Lighting error: %s", str(e))
        self.view.set_statusbar_text('Error applying Lighting')

    def _set_lighting(self, lighting_modes: LightingModes) -> None:
        logo_mode_id = self.view.get_logo_mode_id()
        self._set_lighting_logo(logo_mode_id, lighting_modes)
        ring_mode_id = self.view.get_ring_mode_id()
        self._set_lighting_ring(ring_mode_id, lighting_modes)

    def _set_lighting_logo(self, mode_id: int, lighting_modes: LightingModes) -> None:
        lighting_mode = lighting_modes.modes_logo[mode_id] if mode_id > 0 else None
        if lighting_mode:
            number_of_selected_colors = self.view.get_lighting_logo_spin_button()
            # possible bug with liquidCtl: it doesn't let us send an empty list or a None list...
            colors = self.view.get_logo_colors(number_of_selected_colors) \
                if lighting_mode.max_colors > 0 else LightingColors().add(LightingColor())
            if lighting_mode.speed_enabled:
                speed_id = self.view.get_lighting_logo_speed()
                speed = LightingSpeeds().get(speed_id) if speed_id > 0 else None
            else:
                speed = None
            direction = self.view.get_lighting_logo_direction() \
                if lighting_mode.direction_enabled else None
            settings = LightingSettings.create_logo_settings(lighting_mode, colors, speed, direction)
            self._schedule_lighting_setting(settings)

    def on_lighting_logo_colors_spinbutton_changed(self, spinbutton: Any) -> None:
        self.view.set_lighting_logo_color_buttons_enabled(
            spinbutton.get_value_as_int()
        )

    def on_ring_mode_selected(self, *_: Any) -> None:
        mode_id = self.view.get_ring_mode_id()
        if mode_id > 0:
            self._get_lighting_modes(
            ).subscribe(
                on_next=lambda lighting_modes: self._update_ring_widgets(mode_id, lighting_modes),
                on_error=lambda e: _LOG.exception("Lighting error: %s", str(e))
            )
        else:
            raise IndexError("Ring Mode ID from the ListStore is unreadable")

    def _update_ring_widgets(self, mode_id: int, lighting_modes: LightingModes) -> None:
        chosen_ring_mode = lighting_modes.modes_ring[mode_id]
        self.view.set_lighting_ring_spin_button(chosen_ring_mode)
        self.view.set_lighting_ring_color_buttons_enabled(chosen_ring_mode.min_colors)
        self.view.set_lighting_ring_speed_enabled(chosen_ring_mode.speed_enabled)
        self.view.set_lighting_ring_direction_enabled(chosen_ring_mode.direction_enabled)
        self.view.set_lighting_apply_button_enabled(True)

    def on_lighting_ring_colors_spinbutton_changed(self, spinbutton: Any) -> None:
        self.view.set_lighting_ring_color_buttons_enabled(
            spinbutton.get_value_as_int()
        )

    def _set_lighting_ring(self, mode_id: int, lighting_modes: LightingModes) -> None:
        lighting_mode = lighting_modes.modes_ring[mode_id] if mode_id > 0 else None
        if lighting_mode:
            number_of_selected_colors = self.view.get_lighting_ring_spin_button()
            # possible bug with liquidCtl: it doesn't let us send an empty list or a None list...
            colors = self.view.get_ring_colors(number_of_selected_colors) \
                if lighting_mode.max_colors > 0 else LightingColors().add(LightingColor())
            if lighting_mode.speed_enabled:
                speed_id = self.view.get_lighting_ring_speed()
                speed = LightingSpeeds().get(speed_id) if speed_id > 0 else None
            else:
                speed = None
            direction = self.view.get_lighting_ring_direction() \
                if lighting_mode.direction_enabled else None
            settings = LightingSettings.create_ring_settings(lighting_mode, colors, speed, direction)
            self._schedule_lighting_setting(settings)

    def _schedule_lighting_setting(self, settings: LightingSettings) -> None:
        _LOG.info("Setting lighting: [ Channel: %s, Mode: %s, Speed: %s, Direction: %s, Colors: %s ]",
                  settings.channel.value, settings.mode.name, settings.speed_or_default,
                  settings.direction_or_default, settings.colors.values())
        self._composite_disposable.add(
            self._set_lighting_interactor.execute(
                settings
            ).pipe(
                operators.subscribe_on(self._scheduler),
                operators.observe_on(GtkScheduler(GLib)),
            ).subscribe(on_next=lambda _: self._on_lighting_setting_complete(settings),
                        on_error=lambda e: _LOG.exception("Lighting apply error: %s", str(e))))

    def _on_lighting_setting_complete(self, settings: LightingSettings) -> None:
        self._save_current_lighting_profile(settings)
        self._save_current_lighting_colors(settings)
        self.view.set_statusbar_text('Lighting applied')

    def _save_current_lighting_profile(self, settings: LightingSettings) -> None:
        profile, _ = self._get_current_lighting_profiles(settings.channel)
        if profile:
            profile.mode = settings.mode.mode_id
            profile.speed = settings.speed_id_or_default
            profile.direction = settings.direction_or_default
            profile.save()
        else:
            CurrentLightingProfile.create(
                channel=settings.channel.value,
                mode=settings.mode.mode_id,
                speed=settings.speed_id_or_default,
                direction=settings.direction_or_default
            )

    @staticmethod
    def _save_current_lighting_colors(settings: LightingSettings) -> None:
        CurrentLightingColor.delete().where(
            CurrentLightingColor.channel == settings.channel.value
        ).execute()
        if settings.mode.max_colors > 0:
            for index, lighting_color in enumerate(settings.colors.colors):
                CurrentLightingColor.create(
                    channel=settings.channel.value,
                    index=index,
                    red=lighting_color.red,
                    green=lighting_color.green,
                    blue=lighting_color.blue
                )
