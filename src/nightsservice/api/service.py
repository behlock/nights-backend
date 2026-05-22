"""FastAPI application factory.

Locked-down CORS, trusted-host enforcement, generic exception handler that hides
internal tracebacks from clients (full traceback still goes to the structured
log).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette_graphene3 import GraphQLApp

from nightsservice.settings import get_app_settings

logger = structlog.get_logger(__name__)


@dataclass(frozen=True)
class ApplicationManifest:
    app: GraphQLApp
    url_prefix: str


def get_app(
    gql_apps: Iterable[ApplicationManifest],
    api_debug: bool = False,
) -> FastAPI:
    settings = get_app_settings()
    app = FastAPI(
        debug=api_debug,
        title=settings.SERVICE_NAME,
        version=settings.VERSION,
        docs_url=None if settings.is_production else "/docs",
        redoc_url=None if settings.is_production else "/redoc",
        openapi_url=None if settings.is_production else "/openapi.json",
    )

    for manifest in gql_apps:
        app.add_route(manifest.url_prefix, manifest.app)

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok", "version": settings.VERSION}

    cors_origins = settings.cors_origins_list
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["content-type", "authorization"],
            allow_credentials=False,
            max_age=600,
        )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts_list)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled_exception",
            path=request.url.path,
            method=request.method,
            error=type(exc).__name__,
        )
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    return app
