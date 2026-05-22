from __future__ import annotations

from collections.abc import Iterable

from graphene import BigInt, DateTime, Field, InputObjectType

from nightsservice.api.graphql.types import list_of


class NightsInput(InputObjectType):  # type: ignore[misc]
    class Meta:
        description = "Filter parameters for the nights query."

    area_ids: Iterable[BigInt] = list_of(BigInt, description="Resident Advisor area IDs")
    listing_date_lower_bound: DateTime = Field(
        DateTime,
        description="ISO 8601 lower bound (inclusive) for listing date.",
    )
    listing_date_upper_bound: DateTime = Field(
        DateTime,
        description="ISO 8601 upper bound (inclusive) for listing date.",
    )
