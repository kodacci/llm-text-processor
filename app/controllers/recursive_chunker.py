import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi_restful.cbv import cbv
from pydantic import BaseModel
from starlette.routing import Router

from app.controllers.base_controller import BaseController
from app.services.recursive_chunker import RecursiveChunker

_router = APIRouter()

class SplitRequest(BaseModel):
    text: str

class SplitResponse(BaseModel):
    chunks: list[str]

@cbv(_router)
class RecursiveChunkerController(BaseController):
    def _get_api_version(self) -> str:
        return 'v1'

    def __init__(self):
        self._log = logging.getLogger(__name__)

    def _get_router(self) -> Router:
        return _router

    @_router.post('/chunkers/recursive/split-text', response_model=SplitResponse)
    @inject
    async def split_text(
            self,
            req: SplitRequest,
            recursive_chunker: FromDishka[RecursiveChunker]
    ) -> SplitResponse:
        self._log.info('Splitting text of length %d' % len(req.text))
        chunks = recursive_chunker.split_text(req.text)

        self._log.info('Split text in %d chunks' % len(chunks))
        return SplitResponse(chunks=chunks)