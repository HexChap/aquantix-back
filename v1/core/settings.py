from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

ENVS_PATH = Path("env")

__all__ = [
    "settings"
]


class _SecuritySettings:
    access_token_expire_minutes: int
    secret_key: str
    algorithm: str


# noinspection PyUnboundLocalVariable
class _APISettings(BaseSettings):
    title: str
    version: str = Path("v1")
    build_version: str
    version_path: Path | None = Path(version)


class _Settings(BaseSettings):
    api: _APISettings


_api_settings = _APISettings(
    title="Aquantix API",
    version="1",
    build_version="0",
    version_path=Path("v1")
)

settings = _Settings(
    api=_api_settings
)
