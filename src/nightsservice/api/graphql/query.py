from typing import Any, Optional
import graphene

from graphene import NonNull, ObjectType, ResolveInfo, BigInt
from database.operations import get_nights

from nightsservice.api.graphql.inputs import NightsInput
from nightsservice.api.graphql.schema import Night

from nightsservice.api.graphql.types import non_null_list_of


class NightsResponse(ObjectType):  # type: ignore
    nights = non_null_list_of(Night, description="List of nights")
    total_count = NonNull(BigInt, description="Total number of nights")


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
        nights = get_nights(input)  # type: ignore
        return NightsResponse(nights=nights, total_count=len(nights))
