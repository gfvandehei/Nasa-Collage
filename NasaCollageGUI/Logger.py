import enum


class Logger(object):

    class LoggerTypes(enum.Enum):
        STATUS = "[STATUS]"
        WARNING = "[WARNING]"
        ERROR = "[ERROR]"

    def log(self, ltype: LoggerTypes, message: str):
        print(ltype.value, message)
