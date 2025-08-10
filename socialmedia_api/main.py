import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from socialmedia_api.config import config
from socialmedia_api.database import database
from socialmedia_api.logging_conf import configure_logging
from socialmedia_api.routers.post import post_router
from socialmedia_api.routers.upload import router as upload_router
from socialmedia_api.routers.user import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Hello world")
    try:
        from logtail import LogtailHandler

        logtail_handler = LogtailHandler(source_token=config.LOGTAIL_API_KEY)
        logger.addHandler(logtail_handler)
        logger.setLevel(logging.DEBUG)  # au cas où il est resté à WARNING par défaut
        logger.info("🚀 Test direct Logtail depuis lifespan")
    except Exception as e:
        print("💥 Erreur Logtail :", e)
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(upload_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
