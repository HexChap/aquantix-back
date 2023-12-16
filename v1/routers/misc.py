from fastapi import APIRouter, responses

from v1.core import settings

__tags__ = ["misc"]
__prefix__ = ""

router = APIRouter()


@router.get("/api-info")
async def get_api_info():
    return {
        "api_version": settings.api.version,
        "build_version": settings.api.build_version
    }
