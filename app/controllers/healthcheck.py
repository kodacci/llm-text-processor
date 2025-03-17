from enum import Enum

from fastapi import APIRouter, FastAPI
from fastapi_restful.cbv import cbv
from pydantic import BaseModel
from starlette.routing import Router

from app.controllers.base_controller import BaseController

_router = APIRouter()

class Status(Enum):
    OK = 'OK'
    ERROR = 'ERROR'

class HealthCheckResponse(BaseModel):
    status: Status

@cbv(_router)
class HelloController(BaseController):
    def _get_api_version(self) -> str:
        return 'v1'

    def _get_router(self) -> APIRouter:
        return _router

    def register(self, app: FastAPI):
        app.include_router(self._get_router())

    @_router.get('/healthcheck', response_model=HealthCheckResponse)
    def hello(self):
        return HealthCheckResponse(status=Status.OK)
