from typing import Iterable

from graphene import InputObjectType, String, BigInt

from nightsservice.api.graphql.types import list_of


class NightsInput(InputObjectType):  # type: ignore
    class Meta:
        description = """The areas to restrict events fetching to"""

    area_ids: Iterable[BigInt] = list_of(String, description="A list of area ids")
