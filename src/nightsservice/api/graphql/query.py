from __future__ import annotations

from typing import Any

import graphene
from graphene import ObjectType, ResolveInfo

from database.connection import init_engine
from database.operations import get_nights
from nightsservice.api.graphql.inputs import NightsInput
from nightsservice.api.graphql.schema import Night
from nightsservice.api.graphql.types import non_null_list_of


class NightsResponse(ObjectType):  # type: ignore[misc]
    nights = non_null_list_of(Night, description="List of nights")


class Query(ObjectType):  # type: ignore[misc]
    nights = graphene.Field(
        NightsResponse,
        input=NightsInput(),
        description="Get list of nights, optionally filtered by date range.",
        required=True,
    )

    @staticmethod
    def resolve_nights(
        parent: Any,
        info: ResolveInfo,
        input: NightsInput | None = None,
    ) -> NightsResponse:
        engine = init_engine(is_local=False)
        nights = get_nights(engine=engine, input=input)
        return NightsResponse(nights=nights)
