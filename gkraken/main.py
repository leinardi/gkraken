#!/usr/bin/env python3

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
import signal
import locale
import gettext
import logging
import sys
import gi
from os.path import abspath, join, dirname
from peewee import SqliteDatabase
from rx.disposables import CompositeDisposable

gi.require_version('Gtk', '3.0')
from gi.repository import GLib
from gkraken.repository import KrakenRepository
from gkraken.di import INJECTOR
from gkraken.app import Application

APP = "gkraken"
WHERE_AM_I = abspath(dirname(__file__))
LOCALE_DIR = join(WHERE_AM_I, 'mo')

FORMAT = '%(filename)15s:%(lineno)-4d %(asctime)-15s: %(levelname)s/%(threadName)s(%(process)d) %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger("Rx").setLevel(logging.INFO)
logging.getLogger('injector').setLevel(logging.INFO)
logging.getLogger('peewee').setLevel(logging.INFO)
logging.getLogger('matplotlib').setLevel(logging.INFO)

LOG = logging.getLogger(__name__)

# POSIX locale settings
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP, LOCALE_DIR)

gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)


def __cleanup() -> None:
    LOG.debug("cleanup")
    composite_disposable: CompositeDisposable = INJECTOR.get(CompositeDisposable)
    composite_disposable.dispose()
    database = INJECTOR.get(SqliteDatabase)
    database.close()
    kraken_repository = INJECTOR.get(KrakenRepository)
    kraken_repository.cleanup()
    # futures.thread._threads_queues.clear()


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    LOG.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    __cleanup()
    sys.exit(1)


sys.excepthook = handle_exception


def main() -> int:
    LOG.debug("main")
    application: Application = INJECTOR.get(Application)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, application.quit)
    exit_status = application.run(sys.argv)
    __cleanup()
    return sys.exit(exit_status)


if __name__ == "__main__":
    main()
