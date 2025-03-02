from abc import ABC, abstractmethod

from fastapi import FastAPI, APIRouter

class BaseController(ABC):
    @abstractmethod
    def _get_router(self) -> APIRouter:
        pass

    @abstractmethod
    def _get_api_version(self) -> str:
        pass

    def register(self, app: FastAPI):
        app.include_router(self._get_router(), prefix='/api/' + self._get_api_version())