# This file is part of gkraken.
#
# Copyright (c) 2019 Roberto Leinardi
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
from enum import Enum
from gettext import gettext as _
from typing import Any, Optional, List

from gi.repository import Gtk, Gio, GLib
from injector import inject
from peewee import SqliteDatabase

from gkraken.conf import APP_NAME, APP_ID, APP_VERSION
from gkraken.di import MainBuilder
from gkraken.interactor import UdevInteractor
from gkraken.model import load_db_default_data
from gkraken.model.speed_profile import SpeedProfile
from gkraken.model.speed_step import SpeedStep
from gkraken.model.current_speed_profile import CurrentSpeedProfile
from gkraken.model.setting import Setting
from gkraken.presenter.main import MainPresenter
from gkraken.util.deployment import is_flatpak
from gkraken.util.desktop_entry import set_autostart_entry
from gkraken.util.log import LOG_DEBUG_FORMAT
from gkraken.util.view import build_glib_option
from gkraken.view.main import MainView

LOG = logging.getLogger(__name__)


class Application(Gtk.Application):
    @inject
    def __init__(self,
                 database: SqliteDatabase,
                 view: MainView,
                 presenter: MainPresenter,
                 builder: MainBuilder,
                 udev_interactor: UdevInteractor,
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

        self.add_main_option_entries(self._get_main_option_entries())
        self._view = view
        self._presenter = presenter
        self._presenter.application_quit = self.quit
        self._window: Optional[Gtk.ApplicationWindow] = None
        self._builder: Gtk.Builder = builder
        self._udev_interactor = udev_interactor
        self._start_hidden: bool = False

    def do_activate(self) -> None:
        if not self._window:
            self._builder.connect_signals(self._presenter)
            self._window: Gtk.ApplicationWindow = self._builder.get_object("application_window")
            self._window.set_application(self)
            self._window.show_all()
            self._view.show()
        self._window.present()
        if self._start_hidden:
            self._window.hide()
            self._start_hidden = False

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

        if _Options.HIDE_WINDOW.value in options:
            LOG.debug("Option %s selected", _Options.HIDE_WINDOW.value)
            self._start_hidden = True

        if _Options.AUTOSTART_ON.value in options:
            LOG.debug("Option %s selected", _Options.AUTOSTART_ON.value)
            set_autostart_entry(True)
            start_app = False

        if _Options.AUTOSTART_OFF.value in options:
            LOG.debug("Option %s selected", _Options.AUTOSTART_OFF.value)
            set_autostart_entry(True)
            start_app = False

        if _Options.ADD_UDEV_RULE.value in options:
            LOG.debug("Option %s selected", _Options.ADD_UDEV_RULE.value)
            exit_value += self._udev_interactor.add_udev_rule()
            start_app = False

        if _Options.REMOVE_UDEV_RULE.value in options:
            LOG.debug("Option %s selected", _Options.REMOVE_UDEV_RULE.value)
            exit_value += self._udev_interactor.remove_udev_rule()
            start_app = False

        if start_app:
            self.activate()
        return exit_value

    @staticmethod
    def _get_main_option_entries() -> List[GLib.OptionEntry]:
        options = [
            build_glib_option(_Options.VERSION.value,
                              short_name='v',
                              description="Show the app version"),
            build_glib_option(_Options.DEBUG.value,
                              description="Show debug messages"),
            build_glib_option(_Options.HIDE_WINDOW.value,
                              description="Start with the main window hidden"),
            build_glib_option(_Options.ADD_UDEV_RULE.value,
                              description="Add udev rule to allow execution without root permission"),
            build_glib_option(_Options.REMOVE_UDEV_RULE.value,
                              description="Remove udev rule that allow execution without root permission"),
        ]
        if not is_flatpak():
            options.append(build_glib_option(_Options.AUTOSTART_ON.value,
                                             description="Enable automatic start of the app on login"))
            options.append(build_glib_option(_Options.AUTOSTART_OFF.value,
                                             description="Disable automatic start of the app on login"))
        return options


class _Options(Enum):
    VERSION = 'version'
    DEBUG = 'debug'
    HIDE_WINDOW = 'hide-window'
    AUTOSTART_ON = 'autostart-on'
    AUTOSTART_OFF = 'autostart-off'
    ADD_UDEV_RULE = 'add-udev-rule'
    REMOVE_UDEV_RULE = 'remove-udev-rule'
