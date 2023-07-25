import dotenv

import graphene
from fastapi.applications import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from nightsservice.api import service
from nightsservice.api.graphql.query import Query

APPLICATIONS = frozenset(
    [
        service.ApplicationManifest(
            url_prefix="/graphql",
            app=GraphQLApp(graphene.Schema(query=Query), on_get=make_graphiql_handler()),
        )
    ]
)


def init_app() -> FastAPI:
    dotenv.load_dotenv()
    app = service.get_app(gql_apps=APPLICATIONS)

    return app
