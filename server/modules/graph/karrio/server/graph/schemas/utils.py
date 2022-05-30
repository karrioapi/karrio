import base64
from dataclasses import dataclass, make_dataclass
import typing
import functools
import strawberry
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

Cursor = str
T = typing.TypeVar("T")
GenericType = typing.TypeVar("GenericType")


@dataclass
@strawberry.type
class Connection(typing.Generic[GenericType]):
    """Represents a paginated relationship between two entities

    This pattern is used when the relationship itself has attributes.
    In a Facebook-based domain example, a friendship between two people
    would be a connection that might have a `friendshipStartTime`
    """

    page_info: "PageInfo"
    edges: typing.List["Edge[GenericType]"]


@dataclass
@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination

    Instead of classic offset pagination via `page` and `limit` parameters,
    here we have a cursor of the last object and we fetch items starting from that one

    Read more at:
        - https://graphql.org/learn/pagination/#pagination-and-edges
        - https://relay.dev/graphql/connections.htm
    """

    has_next_page: bool
    has_previous_page: bool
    start_cursor: typing.Optional[str]
    end_cursor: typing.Optional[str]


@dataclass
@strawberry.type
class Edge(typing.Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: GenericType
    cursor: str


def build_entity_cursor(entity: T):
    """Adapt this method to build an *opaque* ID from an instance"""
    entityid = f"{getattr(entity, 'id', id(entity))}".encode("utf-8")
    return base64.b64encode(entityid).decode()


def paginated_connection(
    queryset,
    first: int = 25,
    offset: int = 0,
) -> Connection[T]:
    """A non-trivial implementation should efficiently fetch only
    the necessary books after the offset.
    For simplicity, here we build the list and then slice it accordingly
    """

    # Fetch the requested results plus one, just to calculate `has_next_page`
    # fmt: off
    results = queryset[offset:offset+first+1]
    # fmt: on

    edges: typing.List[typing.Any] = [
        Edge(node=typing.cast(T, entity), cursor=build_entity_cursor(entity))
        for entity in results
    ]
    return Connection(
        page_info=PageInfo(
            has_previous_page=False,
            has_next_page=len(results) > first,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-2].cursor if len(edges) > 1 else None,
        ),
        edges=edges[:-1],
    )


def login_required(func):
    @functools.wraps(func)
    def wrapper(info, *args, **kwargs):
        if info.context.request.user.is_anonymous:
            raise exceptions.AuthenticationFailed(
                _("You are not authenticated"), code="login_required"
            )

        return func(info, *args, **kwargs)

    return wrapper


def password_required(func):
    @functools.wraps(func)
    def wrapper(info, *args, **kwargs):
        password = kwargs.get("password")

        if not info.context.request.user.check_password(password):
            raise exceptions.ValidationError({"password": "Invalid password"})

        return func(info, *args, **kwargs)

    return wrapper
