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
from typing import Any

from gi.repository import GLib
from injector import singleton, inject
from rx import Observable, operators
from rx.disposable import CompositeDisposable
from rx.scheduler.mainloop import GtkScheduler

from gkraken.interactor.get_lighting_modes_interactor import GetLightingModesInteractor
from gkraken.interactor.set_lighting_interactor import SetLightingInteractor
from gkraken.model.lighting_modes import LightingModes
from gkraken.model.lighting_settings import LightingColors, LightingSettings, LightingColor
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
                 composite_disposable: CompositeDisposable,
                 scheduler: Scheduler,
                 ) -> None:
        _LOG.debug("init LightingPresenter ")
        self.view: LightingViewInterface = LightingViewInterface()
        self._set_lighting_interactor = set_lighting_interactor
        self._get_lighting_modes_interactor = get_lighting_modes_interactor
        self._composite_disposable: CompositeDisposable = composite_disposable
        self._scheduler = scheduler.get()

    def load_lighting_modes(self) -> None:
        self._composite_disposable.add(
            self._get_lighting_modes().subscribe(
                on_next=self.view.load_color_modes,
                on_error=lambda e: _LOG.exception("Lighting error: %s", str(e))))

    def _get_lighting_modes(self) -> Observable:
        return self._get_lighting_modes_interactor.execute(
        ).pipe(
            operators.subscribe_on(self._scheduler),
            operators.observe_on(GtkScheduler(GLib)),
        )

    def on_logo_mode_selected(self, *_: Any) -> None:
        mode_id = self.view.get_logo_mode_id()
        self._get_lighting_modes(
        ).subscribe(
            on_next=lambda lighting_modes: self._update_logo_widgets(mode_id, lighting_modes),
            on_error=lambda e: _LOG.exception("Lighting error: %s", str(e))
        )

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
            # possible bug with liquidctl: it doesn't let us send an empty list or a None list...
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
        self._get_lighting_modes(
        ).subscribe(
            on_next=lambda lighting_modes: self._update_ring_widgets(mode_id, lighting_modes),
            on_error=lambda e: _LOG.exception("Lighting error: %s", str(e))
        )

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
            # possible bug with liquidctl: it doesn't let us send an empty list or a None list...
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
                  settings.channel.value, settings.mode, settings.speed, settings.direction, settings.colors.values())
        self._composite_disposable.add(
            self._set_lighting_interactor.execute(
                settings
            ).pipe(
                operators.subscribe_on(self._scheduler),
                operators.observe_on(GtkScheduler(GLib)),
            ).subscribe(on_next=lambda _: self.view.set_statusbar_text('Lighting applied'),
                        on_error=lambda e: _LOG.exception("Lighting apply error: %s", str(e))))
