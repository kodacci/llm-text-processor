from fastapi import FastAPI

from app.controllers.healthcheck import HelloController
from app.controllers.recursive_chunker import RecursiveChunkerController

_controllers = (
    HelloController(),
    RecursiveChunkerController()
)

class ControllersConfig:
    def __init__(self, app: FastAPI) -> None:
        self._app = app

    def apply(self):
        for controller in _controllers:
            controller.register(self._app)