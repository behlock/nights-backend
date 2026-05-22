from typing import Any

import graphene
from graphene import NonNull
from graphene.types.base import BaseType


def list_of[T: BaseType](inner_type: type[T], *args: Any, **kwargs: Any) -> graphene.types.List:
    """Make a Graphene `graphene.List` of non-nullable `inner_type`.
    The parameters are for the List type, not its wrapper, nor the inner type."""
    return graphene.types.List(NonNull(inner_type), *args, **kwargs)


def non_null_list_of[T: BaseType](
    inner_type: type[T], *args: Any, **kwargs: Any
) -> graphene.types.List:
    """Make a Graphene non-null `graphene.List` of non-nullable `inner_type`.
    The parameters are for the List type, not its wrapper, nor the inner type."""
    return NonNull(graphene.types.List(NonNull(inner_type)), *args, **kwargs)
