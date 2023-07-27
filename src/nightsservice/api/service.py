from dataclasses import dataclass
from typing import Iterable, Text


from fastapi.applications import FastAPI
from starlette_graphene3 import GraphQLApp
from starlette.middleware.cors import CORSMiddleware

from nightsservice.config import VERSION, SERVICE_NAME


@dataclass(frozen=True)
class ApplicationManifest:
    app: GraphQLApp
    url_prefix: Text


def get_app(
    gql_apps: Iterable[ApplicationManifest],
    api_debug: bool = False,
) -> FastAPI:
    app = FastAPI(debug=api_debug, title=SERVICE_NAME, version=VERSION)

    for gql_app_manifest in gql_apps:
        app.add_route(gql_app_manifest.url_prefix, gql_app_manifest.app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:3000",
            "https://www.onepointfive.dev",
        ],
        allow_methods=["POST", "GET"],
        allow_headers=["authorization", "content-type"],
    )

    return app
