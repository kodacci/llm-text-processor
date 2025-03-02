import logging

from types import MappingProxyType
from pyaml_env import parse_config

class AppConfig:
    def __init__(self, config_file_name: str) -> None:
        log = logging.getLogger(__name__)
        log.info("Loading application config from file: %s" % config_file_name)
        self._config = MappingProxyType(parse_config(config_file_name))
        log.info("Successfully loaded config file")

    def get(self) -> MappingProxyType:
        return self._config
