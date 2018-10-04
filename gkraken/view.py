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

from gkraken.model import Status
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
        data = {0: 25, 25: 25, 35: 25, 40: 40, 45: 45, 50: 60, 60: 100, 100: 100}

        self.__plot_chart(cooling_fan_scrolled_window, data)
        self.__plot_chart(cooling_pump_scrolled_window, data)

    def show(self) -> None:
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

    @staticmethod
    def __plot_chart(scrolled_window: Gtk.ScrolledWindow, data: Dict[int, int]) -> None:
        figure = Figure(figsize=(8, 6), dpi=72, facecolor="#00000000")
        axis = figure.add_subplot(111)
        names = list(data.keys())
        values = list(data.values())
        axis.plot(names, values, 'o-', linewidth=3.0, markersize=12, antialiased=True)
        axis.grid(True, linestyle=':')
        axis.margins(x=0, y=0.05)
        axis.set_ybound(lower=0)
        axis.set_xbound(20, 70)
        axis.set_facecolor("#00000000")
        axis.set_xlabel('Liquid temperature [°C]')
        axis.set_ylabel('Fan speed [%]')
        figure.subplots_adjust(top=1)
        canvas = FigureCanvas(figure)  # a Gtk.DrawingArea
        canvas.set_size_request(400, 300)
        scrolled_window.add_with_viewport(canvas)
