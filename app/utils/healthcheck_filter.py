import os.path
from logging import Filter, LogRecord


class HealthcheckFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.getMessage().find("/healthcheck") == -1