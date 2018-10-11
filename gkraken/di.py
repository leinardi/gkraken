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

from typing import Optional
from gi.repository import Gtk
from injector import Module, provider, singleton, Injector
from liquidctl.cli import find_all_supported_devices
from liquidctl.driver.kraken_two import KrakenTwoDriver
from peewee import SqliteDatabase
from rx.disposables import CompositeDisposable

from gkraken.conf import APP_PACKAGE_NAME, APP_UI_NAME, APP_DB_NAME
from gkraken.util import get_data_path, get_config_path

LOG = logging.getLogger(__name__)


# pylint: disable=no-self-use
class ProviderModule(Module):
    @singleton
    @provider
    def provide_builder(self) -> Gtk.Builder:
        LOG.debug("provide Gtk.Builder")
        builder = Gtk.Builder()
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_file(get_data_path(APP_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_thread_pool_scheduler(self) -> CompositeDisposable:
        LOG.debug("provide CompositeDisposable")
        return CompositeDisposable()

    @singleton
    @provider
    def provide_database(self) -> SqliteDatabase:
        LOG.debug("provide CompositeDisposable")
        return SqliteDatabase(get_config_path(APP_DB_NAME))

    @provider
    def provide_kraken_two_driver(self) -> Optional[KrakenTwoDriver]:
        LOG.debug("provide KrakenTwoDriver")
        return next((dev for dev in find_all_supported_devices() if isinstance(dev, KrakenTwoDriver)), None)


INJECTOR = Injector(ProviderModule)
