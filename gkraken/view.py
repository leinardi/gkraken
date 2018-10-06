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
from typing import Optional, Dict

from injector import inject, singleton

from gi.repository import Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

from gkraken.model import Status, TemperatureDutyProfileDbModel, FAN_CHANNEL
from gkraken.presenter import Presenter, ViewInterface

LOG = logging.getLogger(__name__)


@singleton
class View(ViewInterface):

    @inject
    def __init__(self,
                 presenter: Presenter,
                 builder: Gtk.Builder,
                 ) -> None:
        LOG.debug("init View")
        self.__presenter: Presenter = presenter
        self.__presenter.view = self
        self.__builder: Gtk.Builder = builder
        self.__init_widgets()

    def __init_widgets(self) -> None:
        # self.refresh_content_header_bar_title()
        self.__statusbar: Gtk.Statusbar = self.__builder.get_object("statusbar")
        self.__cooling_fan_speed: Gtk.Label = self.__builder.get_object("cooling_fan_speed")
        self.__cooling_fan_rpm: Gtk.Label = self.__builder.get_object("cooling_fan_rpm")
        self.__cooling_liquid_temp: Gtk.Label = self.__builder.get_object("cooling_liquid_temp")
        self.__cooling_pump_rpm: Gtk.Label = self.__builder.get_object("cooling_pump_rpm")
        self.__cooling_fan_speed.set_markup("<span size=\"xx-large\">-</span> %")
        cooling_fan_scrolled_window: Gtk.ScrolledWindow = self.__builder.get_object("cooling_fan_scrolled_window")
        cooling_pump_scrolled_window: Gtk.ScrolledWindow = self.__builder.get_object("cooling_pump_scrolled_window")
        self.__init_plot_chart(cooling_fan_scrolled_window, cooling_pump_scrolled_window)


        # data = {0: 25, 25: 25, 35: 25, 40: 40, 45: 45, 50: 60, 60: 100, 100: 100}
        # self.__plot_fan_chart(data)
        # self.__plot_pump_chart(data)


    def show(self) -> None:
        self.__setup_profiles_combobox()
        self.__presenter.on_start()

    def refresh_content_header_bar_title(self) -> None:
        #     contant_stack = self.__builder.get_object("content_stack")
        #     child = contant_stack.get_visible_child()
        #     if child is not None:
        #         title = contant_stack.child_get_property(child, "title")
        #         content_header_bar = self.__builder.get_object("content_header_bar")
        #         content_header_bar.set_title(title)
        pass

    def refresh_status(self, status: Optional[Status]) -> None:
        LOG.debug("view status")
        if status:
            self.__cooling_fan_rpm.set_markup("<span size=\"xx-large\">%s</span> RPM" % status.fan_rpm)
            self.__cooling_liquid_temp.set_markup("<span size=\"xx-large\">%s</span> °C" % status.liquid_temperature)
            self.__cooling_pump_rpm.set_markup("<span size=\"xx-large\">%s</span> RPM" % status.pump_rpm)

    def __setup_profiles_combobox(self) -> None:
        query = TemperatureDutyProfileDbModel.select().where(TemperatureDutyProfileDbModel.channel == FAN_CHANNEL)
        combobox: Gtk.ComboBox = self.__builder.get_object("cooling_fan_profile_combobox")
        if combobox.get_model().iter_n_children() == 0 and query.count():
            profiles_list_store: Gtk.ListStore = self.__builder.get_object("cooling_fan_profile_liststore")
            for profile in query:
                profiles_list_store.append([profile.id, profile.name])

            combobox.set_model(profiles_list_store)
            # if combobox.get_active() == -1:
            #     combobox.set_active(self.__selected_processor[1])
            combobox.set_sensitive(len(profiles_list_store) > 1)

    def __init_plot_chart(self,
                          fan_scrolled_window: Gtk.ScrolledWindow,
                          pump_scrolled_window: Gtk.ScrolledWindow) -> None:
        self.__fan_figure = Figure(figsize=(8, 6), dpi=72, facecolor="#00000000")
        self.__fan_canvas = FigureCanvas(self.__fan_figure)  # a Gtk.DrawingArea+
        self.__fan_axis = self.__fan_figure.add_subplot(111)
        self.__fan_axis.grid(True, linestyle=':')
        self.__fan_axis.margins(x=0, y=0.05)
        self.__fan_axis.set_ybound(lower=0)
        self.__fan_axis.set_xbound(20, 70)
        self.__fan_axis.set_facecolor("#00000000")
        self.__fan_axis.set_xlabel('Liquid temperature [°C]')
        self.__fan_axis.set_ylabel('Fan speed [%]')
        self.__fan_figure.subplots_adjust(top=1)
        self.__fan_canvas.set_size_request(400, 300)
        fan_scrolled_window.add_with_viewport(self.__fan_canvas)
        self.__pump_figure = Figure(figsize=(8, 6), dpi=72, facecolor="#00000000")
        self.__pump_canvas = FigureCanvas(self.__pump_figure)  # a Gtk.DrawingArea+
        self.__pump_axis = self.__pump_figure.add_subplot(111)
        self.__pump_axis.grid(True, linestyle=':')
        self.__pump_axis.margins(x=0, y=0.05)
        self.__pump_axis.set_ybound(lower=0)
        self.__pump_axis.set_xbound(20, 70)
        self.__pump_axis.set_facecolor("#00000000")
        self.__pump_axis.set_xlabel('Liquid temperature [°C]')
        self.__pump_axis.set_ylabel('Pump speed [%]')
        self.__pump_figure.subplots_adjust(top=1)
        self.__pump_canvas.set_size_request(400, 300)
        pump_scrolled_window.add_with_viewport(self.__pump_canvas)

    def __plot_fan_chart(self, data: Dict[int, int]) -> None:
        names = list(data.keys())
        values = list(data.values())
        self.__fan_axis.plot(names, values, 'o-', linewidth=3.0, markersize=12, antialiased=True)

    def __plot_pump_chart(self, data: Dict[int, int]) -> None:
        names = list(data.keys())
        values = list(data.values())
        self.__pump_axis.plot(names, values, 'o-', linewidth=3.0, markersize=12, antialiased=True)
