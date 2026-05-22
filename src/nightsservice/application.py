from __future__ import annotations

import dotenv
import graphene
from fastapi.applications import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from nightsservice.api import service
from nightsservice.api.graphql.query import Query
from nightsservice.logging_config import configure_logging
from nightsservice.settings import get_app_settings


def init_app() -> FastAPI:
    dotenv.load_dotenv()

    settings = get_app_settings()
    configure_logging(level=settings.LOG_LEVEL, is_production=settings.is_production)

    # Disable introspection / GraphiQL in production so the schema isn't exposed.
    on_get = None if settings.is_production else make_graphiql_handler()
    schema = graphene.Schema(query=Query, auto_camelcase=True)

    gql_apps = frozenset(
        [
            service.ApplicationManifest(
                url_prefix="/graphql",
                app=GraphQLApp(schema, on_get=on_get),
            )
        ]
    )

    return service.get_app(gql_apps=gql_apps)
