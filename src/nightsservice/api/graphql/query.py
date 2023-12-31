from typing import Any, Optional
import graphene
from graphene import ObjectType, ResolveInfo

from database.connection import init_engine
from database.operations import get_nights

from nightsservice.api.graphql.inputs import NightsInput
from nightsservice.api.graphql.schema import Night

from nightsservice.api.graphql.types import non_null_list_of


class NightsResponse(ObjectType):  # type: ignore
    nights = non_null_list_of(Night, description="List of nights")


class Query(ObjectType):  # type: ignore
    nights = graphene.Field(
        NightsResponse,
        input=NightsInput(),
        description="Get list of nights for areas",
        required=True,
    )

    @staticmethod
    def resolve_nights(
        parent: Any, info: ResolveInfo, input: Optional[NightsInput] = None
    ) -> NightsResponse:
        engine = init_engine(is_local=False)
        nights = get_nights(engine=engine, input=input)  # type: ignore
        return NightsResponse(nights=nights)
