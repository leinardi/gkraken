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

from typing import Optional, NewType
from gi.repository import Gtk
from injector import Module, provider, singleton, Injector
from liquidctl.driver.kraken2 import Kraken2
from liquidctl.driver.kraken3 import KrakenX3, KrakenZ3
from liquidctl.driver.usb import BaseDriver
from peewee import SqliteDatabase
from rx.disposable import CompositeDisposable
from rx.subject import Subject

from gkraken.conf import APP_PACKAGE_NAME, APP_MAIN_UI_NAME, APP_DB_NAME, APP_EDIT_SPEED_PROFILE_UI_NAME, \
    APP_PREFERENCES_UI_NAME
from gkraken.util.path import get_config_path

_LOG = logging.getLogger(__name__)

SpeedProfileChangedSubject = NewType("SpeedProfileChangedSubject", Subject)
SpeedStepChangedSubject = NewType("SpeedStepChangedSubject", Subject)
MainBuilder = NewType('MainBuilder', Gtk.Builder)
EditSpeedProfileBuilder = NewType('EditSpeedProfileBuilder', Gtk.Builder)
PreferencesBuilder = NewType('PreferencesBuilder', Gtk.Builder)

_UI_RESOURCE_PATH = "/com/leinardi/gkraken/ui/{}"


# pylint: disable=no-self-use
class ProviderModule(Module):
    @singleton
    @provider
    def provide_main_builder(self) -> MainBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = MainBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_MAIN_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_edit_speed_profile_builder(self) -> EditSpeedProfileBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = EditSpeedProfileBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_EDIT_SPEED_PROFILE_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_preferences_builder(self) -> PreferencesBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = PreferencesBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_PREFERENCES_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_thread_pool_scheduler(self) -> CompositeDisposable:
        _LOG.debug("provide CompositeDisposable")
        return CompositeDisposable()

    @singleton
    @provider
    def provide_database(self) -> SqliteDatabase:
        _LOG.debug("provide CompositeDisposable")
        return SqliteDatabase(get_config_path(APP_DB_NAME))

    @provider
    def provide_kraken_driver(self) -> Optional[BaseDriver]:
        _LOG.debug("provide Kraken Driver")
        # return next((dev for dev in find_liquidctl_devices() if isinstance(dev, BaseDriver)), None)
        return next((dev for dev in (
                KrakenZ3.find_supported_devices()
                or KrakenX3.find_supported_devices()
                or Kraken2.find_supported_devices()
        )), None)

    @singleton
    @provider
    def provide_speed_profile_changed_subject(self) -> SpeedProfileChangedSubject:
        return SpeedProfileChangedSubject(Subject())

    @singleton
    @provider
    def provide_speed_step_changed_subject(self) -> SpeedStepChangedSubject:
        return SpeedStepChangedSubject(Subject())


INJECTOR = Injector(ProviderModule)
