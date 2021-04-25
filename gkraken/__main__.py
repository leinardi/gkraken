#!/usr/bin/env python3

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

import gettext
import locale
import logging
import signal
import sys
from os.path import abspath, join, dirname
from typing import Type, Any

import gi
from peewee import SqliteDatabase
from rx.disposable import CompositeDisposable

from gkraken.app import Application
from gkraken.conf import APP_PACKAGE_NAME
from gkraken.di import INJECTOR
from gkraken.repository.kraken_repository import KrakenRepository
from gkraken.util.log import set_log_level

gi.require_version('Gtk', '3.0')
from gi.repository import GLib

WHERE_AM_I = abspath(dirname(__file__))
LOCALE_DIR = join(WHERE_AM_I, 'mo')

set_log_level(logging.INFO)

_LOG = logging.getLogger(__name__)

# POSIX locale settings (for GtkBuilder)
try:
    locale.setlocale(locale.LC_ALL, locale.getlocale())
    locale.bindtextdomain(APP_PACKAGE_NAME, LOCALE_DIR)
except AttributeError as e:
    # Python built without gettext support doesn't have bindtextdomain()
    # and textdomain()
    print("Couldn't bind the gettext translation domain. Some translations"
    " won't work. Error: \n{}".format(e))

gettext.bindtextdomain(APP_PACKAGE_NAME, LOCALE_DIR)
gettext.textdomain(APP_PACKAGE_NAME)


def _cleanup() -> None:
    _LOG.debug("cleanup")
    composite_disposable = INJECTOR.get(CompositeDisposable)
    composite_disposable.dispose()
    database = INJECTOR.get(SqliteDatabase)
    database.close()
    kraken_repository = INJECTOR.get(KrakenRepository)
    kraken_repository.cleanup()
    # futures.thread._threads_queues.clear()


def handle_exception(exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: Any) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    _LOG.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    _cleanup()
    sys.exit(1)


sys.excepthook = handle_exception


def main() -> int:
    _LOG.debug("main")
    application: Application = INJECTOR.get(Application)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, application.quit)
    exit_status = application.run(sys.argv)
    _LOG.info("Shutting down")
    _cleanup()
    return sys.exit(exit_status)


if __name__ == "__main__":
    main()
