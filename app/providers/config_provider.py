import logging
from dishka import Provider, provide, Scope
from app.utils.app_config import AppConfig

class ConfigProvider(Provider):
    def __init__(self, config_file_name: str) -> None:
        super().__init__(scope=Scope.APP)
        self._config = AppConfig(config_file_name)

    @provide(scope=Scope.APP)
    def get_config(self) -> AppConfig:
        return self._config