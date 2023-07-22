from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
import graphene

from nightsservice.api.graphql.query import Query

if __name__ == "__main__":
    schema = graphene.Schema(query=Query)

    app = Starlette()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))

    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
