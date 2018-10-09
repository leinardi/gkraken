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
from gettext import gettext as _
from typing import Any, Optional

from gi.repository import Gtk, Gio, GLib
from injector import inject
from peewee import SqliteDatabase

from gkraken.conf import APP_NAME, APP_ID
from gkraken.model import SpeedProfile, SpeedStep, Setting, CurrentSpeedProfile
from gkraken.presenter import Presenter
from gkraken.util import load_db_default_data
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

        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)
        self.__view = view
        self.__presenter = presenter
        self.__presenter.application_quit = self.quit
        self.__window: Optional[Gtk.ApplicationWindow] = None
        self.__builder: Gtk.Builder = builder

    def do_activate(self) -> None:
        if not self.__window:
            self.__builder.connect_signals(self.__presenter)
            self.__window: Gtk.ApplicationWindow = self.__builder.get_object("application_window")
            self.__window.set_application(self)
            self.__window.show_all()
            self.__view.show()
        self.__window.present()

    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "test" in options:
            # This is printed on the main instance
            print("Test argument recieved: %s" % options["test"])

        self.activate()
        return 0
