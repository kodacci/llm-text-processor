import logging
from logging import Logger
from dishka import Provider, Scope, provide


class LoggerProvider(Provider):
    def __init__(self) -> None:
        super.__init__(scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_logger(self, name: str) -> Logger:
        return logging.getLogger(name)