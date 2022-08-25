import asyncio
import sys

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logger import logger
from app.tasks import check_scouts
from app.discord_commands import run_bot

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure ngrok for local dev
if settings.USE_NGROK and False:
    from pyngrok import ngrok

    ngrok.set_auth_token(settings.NGROK_TOKEN)
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
    public_url = ngrok.connect(port, hostname="mtgscout.api").public_url
    logger.info(f'ngrok tunnel "{public_url}" -> "http://127.0.0.1:{port}"')
    settings.SERVER_HOST = public_url

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

asyncio.create_task(run_bot())


@app.on_event("startup")
@repeat_every(seconds=60 * 60, logger=logger)
def check_scouts_task() -> None:
    check_scouts()
