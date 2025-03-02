from dishka import Provider, provide, Scope

from app.utils.app_config import AppConfig
from app.services.recursive_chunker import RecursiveChunker


class RecursiveChunkerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_chunker(self, config: AppConfig) -> RecursiveChunker:
        params = config.get()['chunkers']['recursive']
        return RecursiveChunker(int(params['chunk-size']), int(params['chunk-overlap']))