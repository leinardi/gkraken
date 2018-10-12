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
import sys
from enum import Enum
from gettext import gettext as _
from typing import Any, Optional, List

from gi.repository import Gtk, Gio, GLib
from injector import inject
from peewee import SqliteDatabase

from gkraken.conf import APP_NAME, APP_ID, APP_VERSION
from gkraken.model import SpeedProfile, SpeedStep, Setting, CurrentSpeedProfile, load_db_default_data
from gkraken.presenter import Presenter
from gkraken.util import build_glib_option, add_udev_rule, remove_udev_rule, LOG_DEBUG_FORMAT
from gkraken.view import View

LOG = logging.getLogger(__name__)


class Application(Gtk.Application):
    @inject
    def __init__(self,
                 database: SqliteDatabase,
                 view: View,
                 presenter: Presenter,
                 builder: Gtk.Builder,
                 *args: Any,
                 **kwargs: Any) -> None:
        LOG.debug("init Application")
        GLib.set_application_name(_(APP_NAME))
        super().__init__(*args, application_id=APP_ID,
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)

        database.connect()
        database.create_tables([SpeedProfile, SpeedStep, CurrentSpeedProfile, Setting])

        if SpeedProfile.select().count() == 0:
            load_db_default_data()

        self.add_main_option_entries(self.__get_main_option_entries())
        self.__view = view
        self.__presenter = presenter
        self.__presenter.application_quit = self.quit
        self.__window: Optional[Gtk.ApplicationWindow] = None
        self.__builder: Gtk.Builder = builder
        self.__start_hidden: bool = False

    def do_activate(self) -> None:
        if not self.__window:
            self.__builder.connect_signals(self.__presenter)
            self.__window: Gtk.ApplicationWindow = self.__builder.get_object("application_window")
            self.__window.set_application(self)
            self.__window.show_all()
            self.__view.show()
        self.__window.present()
        if self.__start_hidden:
            self.__window.hide()
            self.__start_hidden = False

    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        start_app = True
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        exit_value = 0

        if _Options.VERSION.value in options:
            LOG.debug("Option %s selected", _Options.VERSION.value)
            print(APP_VERSION)
            start_app = False

        if _Options.DEBUG.value in options:
            logging.getLogger().setLevel(logging.DEBUG)
            for handler in logging.getLogger().handlers:
                handler.formatter = logging.Formatter(LOG_DEBUG_FORMAT)
            LOG.debug("Option %s selected", _Options.DEBUG.value)

        if _Options.MINIMIZED.value in options:
            LOG.debug("Option %s selected", _Options.MINIMIZED.value)
            self.__start_hidden = True

        if _Options.UDEV_ADD_RULE.value in options:
            LOG.debug("Option %s selected", _Options.UDEV_ADD_RULE.value)
            exit_value += add_udev_rule()
            start_app = False

        if _Options.UDEV_REMOVE_RULE.value in options:
            LOG.debug("Option %s selected", _Options.UDEV_REMOVE_RULE.value)
            exit_value += remove_udev_rule()
            start_app = False

        if start_app:
            self.activate()
        return exit_value

    @staticmethod
    def __get_main_option_entries() -> List[GLib.OptionEntry]:
        options = [
            build_glib_option(_Options.VERSION.value,
                              short_name='v',
                              description="Show the app version"),
            build_glib_option(_Options.DEBUG.value,
                              description="Show debug messages"),
            build_glib_option(_Options.MINIMIZED.value,
                              short_name='m',
                              description="Start minimized to the notification area"),
        ]
        linux_options = [

            build_glib_option(_Options.UDEV_ADD_RULE.value,
                              description="Add udev rule to allow execution without root permission"),
            build_glib_option(_Options.UDEV_REMOVE_RULE.value,
                              description="Remove udev rule that allow execution without root permission"),
        ]

        if sys.platform.startswith('linux'):
            options += linux_options

        return options


class _Options(Enum):
    VERSION = 'version'
    DEBUG = 'debug'
    MINIMIZED = 'minimized'
    UDEV_ADD_RULE = 'udev-add-rule'
    UDEV_REMOVE_RULE = 'udev-remove-rule'
