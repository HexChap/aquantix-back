import importlib
import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn as uvicorn
from fastapi import FastAPI

from v1.core.firebase import init_firebase
from v1.core.settings import settings

DB_URL_FMT = "{driver}://{user}:{password}@{host}:{port}/{database}"


def include_routers(app: FastAPI):
    """
    Routers must contain the variables **__tags__** and **__prefix__** \n
    If router's name starts with "_" it won't be included

    :param app: Instance of FastAPI class
    :return: None
    """
    for module_name in os.listdir(settings.api.version_path / "routers"):
        if module_name.startswith("_") or not module_name.endswith(".py"):
            continue

        module = importlib.import_module(f"v1.routers.{module_name.removesuffix('.py')}")

        app.include_router(
            module.router, tags=module.__tags__, prefix=module.__prefix__
        )


@asynccontextmanager
async def on_startup(app: FastAPI):
    # print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    init_firebase()
    include_routers(app)

    yield


application = FastAPI(
    title=settings.api.title,
    version=f"{settings.api.version}.{settings.api.build_version}",
    lifespan=on_startup
)


if __name__ == "__main__":
    uvicorn.run("main:application", reload=True)
