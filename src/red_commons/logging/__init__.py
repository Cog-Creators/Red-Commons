import asyncio
import contextlib
import logging

VERBOSE = logging.DEBUG - 3
TRACE = logging.DEBUG - 5

__all__ = [
    "RedTraceLogger",
    "VERBOSE",
    "TRACE",
    "update_logger",
    "task_callback_critical",
    "task_callback_exception",
    "task_callback_warning",
    "task_callback_debug",
    "task_callback_verbose",
    "task_callback_trace",
]


class RedTraceLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

        logging.addLevelName(VERBOSE, "VERBOSE")
        logging.addLevelName(TRACE, "TRACE")

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)


def update_logger():
    if not isinstance(logging.getLoggerClass(), RedTraceLogger):
        logging.setLoggerClass(RedTraceLogger)


_log = logging.getLogger("red.commons.logging")


def task_callback_critical(task: asyncio.Task) -> None:
    with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
        if exc := task.exception():
            _log.critical("%s raised an Exception", task.get_name(), exc_info=exc)


def task_callback_exception(task: asyncio.Task) -> None:
    with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
        if exc := task.exception():
            _log.exception("%s raised an Exception", task.get_name(), exc_info=exc)


def task_callback_warning(task: asyncio.Task) -> None:
    with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
        if exc := task.exception():
            _log.warning("%s raised an Exception", task.get_name(), exc_info=exc)


def task_callback_debug(task: asyncio.Task) -> None:
    with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
        if exc := task.exception():
            _log.debug("%s raised an Exception", task.get_name(), exc_info=exc)


def task_callback_verbose(task: asyncio.Task) -> None:
    with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
        if exc := task.exception():
            _log.verbose("%s raised an Exception", task.get_name(), exc_info=exc)


def task_callback_trace(task: asyncio.Task) -> None:
    with contextlib.suppress(asyncio.CancelledError, asyncio.InvalidStateError):
        if exc := task.exception():
            _log.trace("%s raised an Exception", task.get_name(), exc_info=exc)
