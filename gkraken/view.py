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

import gi
import logging
from typing import Optional, Dict, Any, List, Tuple
from injector import inject, singleton
from gi.repository import Gtk

# AppIndicator3 may not be installed
from gkraken.interactor import SettingsInteractor

try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3
except ImportError:
    AppIndicator3 = None
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

from gkraken.conf import APP_PACKAGE_NAME, APP_ID
from gkraken.model import Status, SpeedProfile, ChannelType
from gkraken.presenter import Presenter, ViewInterface

LOG = logging.getLogger(__name__)
if AppIndicator3 is None:
    LOG.warning("AppIndicator3 is not installed. The app indicator will not be shown.")


# pylint: disable=too-many-instance-attributes
@singleton
class View(ViewInterface):

    @inject
    def __init__(self,
                 presenter: Presenter,
                 builder: Gtk.Builder,
                 settings_interactor: SettingsInteractor,
                 ) -> None:
        LOG.debug('init View')
        self.__presenter: Presenter = presenter
        self.__presenter.view = self
        self.__builder: Gtk.Builder = builder
        self.__settings_interactor = settings_interactor
        self.__init_widgets()

    def __init_widgets(self) -> None:
        # self.refresh_content_header_bar_title()
        self.__window = self.__builder.get_object("application_window")
        self.__settings_dialog: Gtk.Dialog = self.__builder.get_object("settings_dialog")
        self.__app_indicator_menu = self.__builder.get_object("app_indicator_menu")
        self.__statusbar: Gtk.Statusbar = self.__builder.get_object('statusbar')
        self.__context = self.__statusbar.get_context_id(APP_PACKAGE_NAME)
        self.__cooling_fan_speed: Gtk.Label = self.__builder.get_object('cooling_fan_speed')
        self.__cooling_fan_rpm: Gtk.Label = self.__builder.get_object('cooling_fan_rpm')
        self.__cooling_liquid_temp: Gtk.Label = self.__builder.get_object('cooling_liquid_temp')
        self.__cooling_pump_rpm: Gtk.Label = self.__builder.get_object('cooling_pump_rpm')
        self.__firmware_version: Gtk.Label = self.__builder.get_object('firmware_version')
        self.__cooling_fan_combobox: Gtk.ComboBox = self.__builder.get_object('cooling_fan_profile_combobox')
        self.__cooling_fan_liststore: Gtk.ListStore = self.__builder.get_object('cooling_fan_profile_liststore')
        self.__cooling_pump_combobox: Gtk.ComboBox = self.__builder.get_object('cooling_pump_profile_combobox')
        self.__cooling_pump_liststore: Gtk.ListStore = self.__builder.get_object('cooling_pump_profile_liststore')
        cooling_fan_scrolled_window: Gtk.ScrolledWindow = self.__builder.get_object('cooling_fan_scrolled_window')
        cooling_pump_scrolled_window: Gtk.ScrolledWindow = self.__builder.get_object('cooling_pump_scrolled_window')
        self.__cooling_fan_apply_button: Gtk.Button = self.__builder.get_object('cooling_fan_apply_button')
        self.__cooling_pump_apply_button: Gtk.Button = self.__builder.get_object('cooling_pump_apply_button')
        self.__init_plot_charts(cooling_fan_scrolled_window, cooling_pump_scrolled_window)

    def show(self) -> None:
        self.__presenter.on_start()
        self.__init_app_indicator()

    def __init_app_indicator(self) -> None:
        self.__app_indicator: Optional[AppIndicator3.Indicator] = None
        if AppIndicator3:
            icon_theme = Gtk.IconTheme.get_default()
            icon_name = icon_theme.lookup_icon('weather-showers-symbolic', 16, 0).get_filename()
            self.__app_indicator = AppIndicator3.Indicator \
                .new(APP_ID, icon_name, AppIndicator3.IndicatorCategory.HARDWARE)
            self.__app_indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
            self.__app_indicator.set_menu(self.__app_indicator_menu)

    def toggle_window_visibility(self) -> None:
        if self.__window.props.visible:
            self.__window.hide()
        else:
            self.__window.show()

    def show_add_speed_profile_dialog(self, channel: ChannelType) -> None:
        LOG.debug("view show_add_speed_profile_dialog %s", channel.name)

    def show_settings_dialog(self) -> None:
        self.__settings_dialog.show()

    def hide_settings_dialog(self) -> None:
        self.__settings_dialog.hide()

    def set_statusbar_text(self, text: str) -> None:
        self.__statusbar.remove_all(self.__context)
        self.__statusbar.push(self.__context, text)

    def refresh_content_header_bar_title(self) -> None:
        #     contant_stack = self.__builder.get_object("content_stack")
        #     child = contant_stack.get_visible_child()
        #     if child is not None:
        #         title = contant_stack.child_get_property(child, "title")
        #         content_header_bar = self.__builder.get_object("content_header_bar")
        #         content_header_bar.set_title(title)
        pass

    def refresh_status(self, status: Optional[Status]) -> None:
        LOG.debug('view status')
        if status:
            self.__cooling_fan_rpm.set_markup("<span size=\"xx-large\">%s</span> RPM" % status.fan_rpm)
            self.__cooling_fan_speed.set_markup("<span size=\"xx-large\">%s</span> %%" %
                                                ('-' if status.fan_speed is None else status.fan_speed))
            self.__cooling_liquid_temp.set_markup("<span size=\"xx-large\">%s</span> °C" % status.liquid_temperature)
            self.__cooling_pump_rpm.set_markup("<span size=\"xx-large\">%s</span> RPM" % status.pump_rpm)
            self.__firmware_version.set_label("firmware version %s" % status.firmware_version)
            if self.__app_indicator:
                if self.__settings_interactor.get_bool('settings_show_app_indicator'):
                    self.__app_indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
                else:
                    self.__app_indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
                if self.__settings_interactor.get_bool('settings_app_indicator_show_water_temp'):
                    self.__app_indicator.set_label("  %s°C" % status.liquid_temperature, "  XX°C")
                else:
                    self.__app_indicator.set_label("", "")

    def refresh_chart(self, profile: SpeedProfile) -> None:
        if profile.channel == ChannelType.FAN.value:
            self.__plot_fan_chart(self.__get_speed_profile_data(profile))
        elif profile.channel == ChannelType.PUMP.value:
            self.__plot_pump_chart(self.__get_speed_profile_data(profile))
        else:
            raise ValueError("Unknown channel: %s" % profile.channel)

    @staticmethod
    def __get_speed_profile_data(profile: SpeedProfile) -> Dict[int, int]:
        data = {p.temperature: p.duty for p in profile.steps}
        if profile.single_step:
            data.update({60: profile.steps[0].duty})
        else:
            data.update({60: 100})
        return data

    def refresh_profile_combobox(self, channel: ChannelType, data: List[Tuple[int, str]],
                                 active: Optional[int]) -> None:
        if channel is ChannelType.FAN:
            for item in data:
                self.__cooling_fan_liststore.append([item[0], item[1]])
            self.__cooling_fan_combobox.set_model(self.__cooling_fan_liststore)
            self.__cooling_fan_combobox.set_sensitive(len(self.__cooling_fan_liststore) > 1)
            if active is not None:
                self.__cooling_fan_combobox.set_active(active)
        elif channel is ChannelType.PUMP:
            for item in data:
                self.__cooling_pump_liststore.append([item[0], item[1]])
            self.__cooling_pump_combobox.set_model(self.__cooling_pump_liststore)
            self.__cooling_pump_combobox.set_sensitive(len(self.__cooling_pump_liststore) > 1)
            if active is not None:
                self.__cooling_pump_combobox.set_active(active)
        else:
            raise ValueError("Unknown channel: %s" % channel.name)

    def set_apply_button_enabled(self, channel: ChannelType, enabled: bool) -> None:
        if channel is ChannelType.FAN:
            self.__cooling_fan_apply_button.set_sensitive(enabled)
        elif channel is ChannelType.PUMP:
            self.__cooling_pump_apply_button.set_sensitive(enabled)
        else:
            raise ValueError("Unknown channel: %s" % channel.name)

    # pylint: disable=attribute-defined-outside-init
    def __init_plot_charts(self,
                           fan_scrolled_window: Gtk.ScrolledWindow,
                           pump_scrolled_window: Gtk.ScrolledWindow) -> None:
        self.__fan_figure = Figure(figsize=(8, 6), dpi=72, facecolor='#00000000')
        self.__fan_canvas = FigureCanvas(self.__fan_figure)  # a Gtk.DrawingArea+
        self.__fan_axis = self.__fan_figure.add_subplot(111)
        self.__fan_line, = self.__init_plot_chart(
            fan_scrolled_window,
            self.__fan_figure,
            self.__fan_canvas,
            self.__fan_axis
        )

        self.__pump_figure = Figure(figsize=(8, 6), dpi=72, facecolor='#00000000')
        self.__pump_canvas = FigureCanvas(self.__pump_figure)  # a Gtk.DrawingArea+
        self.__pump_axis = self.__pump_figure.add_subplot(111)
        self.__pump_line, = self.__init_plot_chart(
            pump_scrolled_window,
            self.__pump_figure,
            self.__pump_canvas,
            self.__pump_axis
        )

    def refresh_settings(self, settings: Dict[str, Any]) -> None:
        for key, value in settings.items():
            if isinstance(value, bool):
                switch: Gtk.Switch = self.__builder.get_object(key + '_switch')
                switch.set_active(value)

    @staticmethod
    def __init_plot_chart(fan_scrolled_window: Gtk.ScrolledWindow,
                          figure: Figure,
                          canvas: FigureCanvas,
                          axis: Axes) -> Any:
        axis.grid(True, linestyle=':')
        axis.margins(x=0, y=0.05)
        axis.set_facecolor('#00000000')
        axis.set_xlabel('Liquid temperature [°C]')
        axis.set_ylabel('Fan speed [%]')
        figure.subplots_adjust(top=1)
        canvas.set_size_request(400, 300)
        fan_scrolled_window.add_with_viewport(canvas)
        # Returns a tuple of line objects, thus the comma
        lines = axis.step([], [], 'o-', where='post', linewidth=3.0, markersize=8, antialiased=True)
        axis.set_ybound(lower=0, upper=105)
        axis.set_xbound(20, 60)
        figure.canvas.draw()
        return lines

    def __plot_fan_chart(self, data: Dict[int, int]) -> None:
        temperature = list(data.keys())
        duty = list(data.values())
        self.__fan_line.set_xdata(temperature)
        self.__fan_line.set_ydata(duty)
        self.__fan_canvas.draw()
        self.__fan_canvas.flush_events()

    def __plot_pump_chart(self, data: Dict[int, int]) -> None:
        temperature = list(data.keys())
        duty = list(data.values())
        self.__pump_line.set_xdata(temperature)
        self.__pump_line.set_ydata(duty)
        self.__pump_canvas.draw()
        self.__pump_canvas.flush_events()
