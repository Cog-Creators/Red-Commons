import logging
from types import TracebackType
from typing import Mapping, Optional, Tuple, Type, Union

__all__ = ("RedTraceLogger", "VERBOSE", "TRACE", "maybe_update_logger_class", "getLogger")

VERBOSE = logging.DEBUG - 3
TRACE = logging.DEBUG - 5

EXEC_INFO_TYPE = Union[
    bool,
    Tuple[Type[BaseException], BaseException, Optional[TracebackType]],
    Tuple[None, None, None],
    BaseException,
]


class RedTraceLogger(logging.Logger):
    def verbose(
        self,
        msg: object,
        *args: object,
        exc_info: Optional[EXEC_INFO_TYPE] = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        """
        Log 'msg % args' with severity 'VERBOSE'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.verbose("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if self.isEnabledFor(VERBOSE):
            self._log(
                VERBOSE,
                msg,
                args,
                exc_info=exc_info,
                stack_info=stack_info,
                extra=extra,
                stacklevel=stacklevel,
            )

    def trace(
        self,
        msg: object,
        *args: object,
        exc_info: Optional[EXEC_INFO_TYPE] = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        """
        Log 'msg % args' with severity 'TRACE'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.trace("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if self.isEnabledFor(TRACE):
            self._log(
                TRACE,
                msg,
                args,
                exc_info=exc_info,
                stack_info=stack_info,
                extra=extra,
                stacklevel=stacklevel,
            )


def maybe_update_logger_class() -> None:
    """Conditionally update the Logger class returned by `logging.getLogger()` to RedTraceLogger"""
    if not issubclass(logging.getLoggerClass(), RedTraceLogger):
        logging.addLevelName(VERBOSE, "VERBOSE")
        logging.addLevelName(TRACE, "TRACE")
        logging.setLoggerClass(RedTraceLogger)


def getLogger(name: Optional[str] = None) -> RedTraceLogger:
    """A typed version of `logging.getLogger()`"""
    logger: RedTraceLogger = logging.getLogger(name)  # type: ignore
    return logger
