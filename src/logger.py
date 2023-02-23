"""
As of now the only purpose of this module is to provide us with a logging interface named
logger, this can be used to log information using various levels: info, error, debug, warning, critical
this will later be expanded to also include configuration options.
"""
from enum import Enum
import datetime
from colorama import Fore


class LogLevel(Enum):
    """
    This class works as an enumeration provider for Logger class
    it provides 4 levels in which log information can be reported
    """
    INFO = 0
    """This is used to relay normal informtion that assures proper working of the application"""
    WARNING = 1
    """This is used to relay events which need to be noted but do not have adverse affet on application"""
    ERROR = 2
    """This is used to relay events which are tolerable errors but need to be reported"""
    CRITICAL = 3
    """This is used to relay events that can cause the appliation to crash"""
    DEBUG = 4
    """This is used to debug and display some intenal structure of an object"""


class Logger:
    """
    A Logger object is used to log events to either a file or to STDOUT
    it provides all the levels of logging available in LogLevel enum class
    Basic usage:
    ```python
    # leave file name empty if you want to write to STDOUT
    logger = Logger("<filename>")
    logger.info("some information to log inforamtional events")
    logger.warn("some information to log warning events")
    logger.error("some information to log error events")
    logger.critical("some information to log critical events")
    logger.log(LogLevel.INFO, "some log info")
    ```
    """

    # TODO: explain the usage of self.file here
    def __init__(self, file: str | None = None) -> None:
        if file == None:
            self.file = "stdout"
        else:
            self.file = file

    def info(self, *args) -> None:
        date = datetime.datetime.now()
        args = "".join(str(a) for a in args)
        if self.file == "stdout":
            print(f"{Fore.LIGHTGREEN_EX}INFO{Fore.RESET} : [{date}] : ", args)
        else:
            with open(self.file, 'w') as f:
                f.write(f"INFO : [{date}] : {args}\n")

    def warn(self, *args) -> None:
        date = datetime.datetime.now()
        args = "".join(str(a) for a in args)
        if self.file == "stdout":
            print(
                f"{Fore.LIGHTYELLOW_EX}WARNING {Fore.RESET}: [{date}] : ", args)
        else:
            with open(self.file, 'w') as f:
                f.write(f"WARNING : [{date}] : {args}\n")

    def error(self, *args) -> None:
        date = datetime.datetime.now()
        args = "".join(str(a) for a in args)
        if self.file == "stdout":
            print(f"{Fore.LIGHTRED_EX}ERROR {Fore.RESET}: [{date}] : ", args)
        else:
            with open(self.file, 'w') as f:
                f.write(f"ERROR : [{date}] : {args}\n")

    def critical(self, *args) -> None:
        date = datetime.datetime.now()
        args = "".join(str(a) for a in args)
        if self.file == "stdout":
            print(f"{Fore.RED}CRITICAL {Fore.RESET}: [{date}] : ", args)
        else:
            with open(self.file, 'w') as f:
                f.write(f"CRITICAL : [{date}] : {args}\n")

    def debug(self, *args) -> None:
        date = datetime.datetime.now()
        args = "".join(str(a) for a in args)
        if self.file == "stdout":
            print(f"{Fore.LIGHTBLUE_EX}DEBUG {Fore.RESET}: [{date}] : ", args)
        else:
            with open(self.file, 'w') as f:
                f.write(f"DEBUG : [{date}] : {args}\n")

    def log(self, log_type: LogLevel, *args) -> None:
        """
        TODO: write documentation
        """
        args = "".join(str(a) for a in args)
        if log_type == LogLevel.INFO:
            self.info(args)
        elif log_type == LogLevel.WARNING:
            self.warn(args)
        elif log_type == LogLevel.ERROR:
            self.error(args)
        elif log_type == LogLevel.CRITICAL:
            self.critical(args)
        elif log_type == LogLevel.DEBUG:
            self.debug(args)
