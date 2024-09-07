"""
Exception handling and logging
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import json

# import jwt
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv

load_dotenv()

api_prefix = "/api/v1/custom-stripe"

app = FastAPI(openapi_url=api_prefix + "/openapi.json", docs_url=api_prefix + "/docs")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

security = HTTPBearer()
logger = logging.getLogger(__name__)

log_level = os.getenv(
    "LOG_LEVEL", "WARNING"
)  # Default to WARNING if LOG_LEVEL is not set
logger.setLevel(logging.getLevelName(log_level))
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(process)d] [%(filename)s: %(funcName)s: %(lineno)s] - %(message)s"
)
os.makedirs("logs/", exist_ok=True)
handler = RotatingFileHandler(f"logs/{__name__}.log", maxBytes=200000, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)


class AppState:
    """
    Application state
    """

    def __init__(self) -> None:
        """
        Initialize application state. Just in case we need to store some global state in the future
        """
        self.user_id = None
        self.is_admin = None


@app.on_event("startup")
async def startup() -> None:
    """
    Startup event
    """
    app.state.app_state = AppState()


@app.exception_handler(Exception)
async def exception_callback(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch all exceptions and log them
    """
    logger.error(f"Error: {str(exc)} <> from host {request.client.host}")
    return JSONResponse({"details": str(exc)}, status_code=500)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Catch all HTTPExceptions and log them
    """
    logger.error(f"Error: {str(exc)} <> from host {request.client.host}")
    return JSONResponse(status_code=exc.status_code, content={"details": exc.detail})
