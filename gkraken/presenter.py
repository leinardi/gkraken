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
import multiprocessing
from typing import Optional, Any

from injector import inject, singleton
from rx import Observable
from rx.concurrency import GtkScheduler, ThreadPoolScheduler
from rx.concurrency.schedulerbase import SchedulerBase
from rx.disposables import CompositeDisposable

from gkraken.interactor import GetStatusInteractor
from gkraken.model import Status

REFRESH_INTERVAL_IN_MS = 2000
LOG = logging.getLogger(__name__)


class ViewInterface:
    def init_system_info(self) -> None:
        raise NotImplementedError()

    def refresh_status(self, status: Status) -> None:
        raise NotImplementedError()

    def refresh_content_header_bar_title(self) -> None:
        raise NotImplementedError()


@singleton
class Presenter:
    @inject
    def __init__(self,
                 get_status_interactor: GetStatusInteractor,
                 composite_disposable: CompositeDisposable,
                 ) -> None:
        LOG.debug("init Presenter ")
        self.view: ViewInterface = ViewInterface()
        self.__get_status_interactor = get_status_interactor
        self.__composite_disposable: CompositeDisposable = composite_disposable

    def on_start(self) -> None:
        scheduler = ThreadPoolScheduler(multiprocessing.cpu_count())
        self.__start_refresh(scheduler)

    def __start_refresh(self, scheduler: SchedulerBase) -> None:
        LOG.debug("start refresh")
        self.__composite_disposable \
            .add(Observable
                 .interval(REFRESH_INTERVAL_IN_MS, scheduler=scheduler)
                 .start_with(0)
                 .subscribe_on(scheduler)
                 .flat_map(lambda _: self.__get_status())
                 .observe_on(GtkScheduler())
                 .subscribe(on_next=lambda status: self.view.refresh_status(status),
                            on_error=lambda e: LOG.exception("Refresh error: %s", str(e)))
                 )

    def on_stack_visible_child_changed(self, *_: Any) -> None:
        self.view.refresh_content_header_bar_title()

    # @staticmethod
    # def __log_exception_return_system_info_observable(ex: Exception) -> Observable:
    #     LOG.exception("Err = %s", ex)
    #     return Observable.just(system_info)

    def __get_status(self) -> Observable:
        return self.__get_status_interactor.execute()  # \
        # .catch_exception(lambda ex: self.__log_exception_return_system_info_observable(system_info, ex))
