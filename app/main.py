import uvicorn
from contextlib import asynccontextmanager
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.controllers.controllers_config import ControllersConfig
from app.providers.config_provider import ConfigProvider
from app.providers.recursive_chunker_provider import RecursiveChunkerProvider

CONFIG_FILE_NAME = 'app/config/application.yaml'

@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):
    yield
    await fast_api_app.state.dishka_container.close()

if __name__ == '__main__':
    config_provider = ConfigProvider(CONFIG_FILE_NAME)
    config = config_provider.get_config()

    # Main application
    app = FastAPI(lifespan=lifespan)
    controllers_config = ControllersConfig(app)
    controllers_config.apply()

    container = make_async_container(config_provider, RecursiveChunkerProvider())
    setup_dishka(container=container, app=app)

    # Uvicorn server
    uvicorn_config = config.get()['server']['uvicorn']
    uvicorn.run(
        app,
        host=uvicorn_config['host'],
        port=uvicorn_config['port'],
        log_config='app/config/logging.yaml'
    )