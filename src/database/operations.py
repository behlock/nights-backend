"""Database operations using SQLAlchemy 2.0 ``select()`` API.

``get_nights`` previously executed N+1 queries (one per related table per night)
and ignored every filter on its input. It now eager-loads relationships via
``selectinload`` and applies the GraphQL input filters.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import structlog
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, selectinload

from database.connection import session_scope
from database.model import (
    Artists,
    Countries,
    Genres,
    NightImages,
    Nights,
    Promoters,
    Tickets,
    Venues,
)
from nightsservice.api.graphql.inputs import NightsInput
from nightsservice.api.graphql.schema import (
    Artist,
    Country,
    Genre,
    Night,
    NightImage,
    Promoter,
    Ticket,
    Venue,
)

logger = structlog.get_logger(__name__)


def _country_to_dto(db_country: Countries) -> Country:
    return Country(
        country_id=db_country.id,
        ra_id=db_country.ra_id,
        name=db_country.name,
        url_code=db_country.url_code,
    )


def _venue_to_dto(db_venue: Venues) -> Venue:
    return Venue(
        venue_id=db_venue.id,
        ra_id=db_venue.ra_id,
        name=db_venue.name,
        address=db_venue.address,
    )


def _image_to_dto(db_image: NightImages) -> NightImage:
    return NightImage(night_image_id=db_image.id, url=db_image.image_url)


def _ticket_to_dto(db_ticket: Tickets) -> Ticket:
    return Ticket(
        ticket_id=db_ticket.id,
        title=db_ticket.title,
        price=db_ticket.price,
        on_sale_from=db_ticket.on_sale_from,
        valid_type=db_ticket.valid_type,
    )


def _promoter_to_dto(db_promoter: Promoters) -> Promoter:
    return Promoter(
        promoter_id=db_promoter.id,
        ra_id=db_promoter.ra_id,
        name=db_promoter.name,
    )


def _artist_to_dto(db_artist: Artists) -> Artist:
    return Artist(artist_id=db_artist.id, ra_id=db_artist.ra_id, name=db_artist.name)


def _genre_to_dto(db_genre: Genres) -> Genre:
    return Genre(genre_id=db_genre.id, ra_id=db_genre.ra_id or "", name=db_genre.name)


def _night_to_dto(db_night: Nights) -> Night:
    return Night(
        night_id=db_night.id,
        ra_id=db_night.ra_id,
        title=db_night.title,
        date=db_night.date,
        content=db_night.content,
        start_time=db_night.start_time,
        end_time=db_night.end_time,
        images=[_image_to_dto(i) for i in db_night.images],
        venue=_venue_to_dto(db_night.venue) if db_night.venue else None,
        tickets=[_ticket_to_dto(t) for t in db_night.tickets],
        promoters=[_promoter_to_dto(p) for p in db_night.promoters],
        artists=[_artist_to_dto(a) for a in db_night.artists],
        genres=[_genre_to_dto(g) for g in db_night.genres],
    )


def get_nights(engine: Engine, input: NightsInput | None) -> list[Night]:
    """Fetch nights with eager-loaded relationships and optional input filters."""
    with session_scope(engine) as session:
        stmt = select(Nights).options(
            selectinload(Nights.images),
            selectinload(Nights.venue),
            selectinload(Nights.tickets),
            selectinload(Nights.promoters),
            selectinload(Nights.artists),
            selectinload(Nights.genres),
        )

        if input is not None:
            stmt = _apply_nights_filters(stmt, input)

        # Hard cap to prevent unbounded queries from a public endpoint.
        stmt = stmt.limit(500)

        db_nights = session.scalars(stmt).all()
        return [_night_to_dto(n) for n in db_nights]


def _apply_nights_filters(stmt: Any, input: NightsInput) -> Any:
    lower = getattr(input, "listing_date_lower_bound", None)
    upper = getattr(input, "listing_date_upper_bound", None)
    if lower:
        try:
            stmt = stmt.where(Nights.date >= datetime.fromisoformat(lower))
        except ValueError:
            logger.warning("nights_filter_bad_lower_bound", value=lower)
    if upper:
        try:
            stmt = stmt.where(Nights.date <= datetime.fromisoformat(upper))
        except ValueError:
            logger.warning("nights_filter_bad_upper_bound", value=upper)
    return stmt


# ---- Setup / write paths used by nightsretrieval ----


def setup_tables(engine: Engine) -> None:
    drop_tables(engine)
    create_tables(engine)


def drop_tables(engine: Engine) -> None:
    from database.model import Base

    Base.metadata.drop_all(engine)


def create_tables(engine: Engine) -> None:
    from database.model import Base

    Base.metadata.create_all(engine)


def get_night_id_from_ra_id(session: Session, ra_id: int) -> int:
    stmt = select(Nights.id).where(Nights.ra_id == ra_id)
    found = session.scalar(stmt)
    if found is None:
        raise ValueError(f"Night with ra_id {ra_id} does not exist")
    return int(found)


def insert_nights_data(engine: Engine, nights: list[dict[str, Any]]) -> None:
    with session_scope(engine) as session:
        _insert_basic_nights_data(session, nights)
        session.flush()
        _insert_additional_nights_data(session, nights)


def _insert_basic_nights_data(session: Session, nights: list[dict[str, Any]]) -> None:
    objects = []
    for night in nights:
        existing = session.scalar(select(Nights).where(Nights.ra_id == night["ra_id"]))
        if existing is None:
            objects.append(
                Nights(
                    ra_id=night["ra_id"],
                    title=night["title"],
                    date=night["date"],
                    content=night["content"],
                    start_time=night["start_time"],
                    end_time=night["end_time"],
                )
            )
    if objects:
        session.add_all(objects)


def _insert_additional_nights_data(session: Session, nights: list[dict[str, Any]]) -> None:
    objects: list[Any] = []
    for night in nights:
        night_id = get_night_id_from_ra_id(session, night["ra_id"])

        for image_url in night["images"]:
            existing_image = session.scalar(
                select(NightImages).where(NightImages.image_url == image_url)
            )
            if existing_image is None:
                objects.append(NightImages(night_id=night_id, image_url=image_url))

        venue_payload = night.get("venue") or {}
        venue_ra_id = venue_payload.get("ra_id")
        if venue_ra_id is not None:
            existing_venue = session.scalar(
                select(Venues).where(Venues.ra_id == str(venue_ra_id))
            )
            if existing_venue is None:
                objects.append(
                    Venues(
                        ra_id=str(venue_ra_id),
                        night_id=night_id,
                        name=venue_payload.get("name", ""),
                        address=venue_payload.get("address"),
                    )
                )

        for promoter in night["promoters"]:
            existing_promoter = session.scalar(
                select(Promoters).where(Promoters.ra_id == str(promoter["ra_id"]))
            )
            if existing_promoter is None:
                objects.append(
                    Promoters(
                        ra_id=str(promoter["ra_id"]),
                        night_id=night_id,
                        name=promoter["name"],
                    )
                )

        for artist in night["artists"]:
            existing_artist = session.scalar(
                select(Artists).where(Artists.ra_id == str(artist["ra_id"]))
            )
            if existing_artist is None:
                objects.append(
                    Artists(
                        ra_id=str(artist["ra_id"]),
                        night_id=night_id,
                        name=artist["name"],
                    )
                )

        for ticket in night["tickets"]:
            objects.append(
                Tickets(
                    night_id=night_id,
                    title=ticket["title"],
                    price=ticket["price"],
                    on_sale_from=ticket["on_sale_from"],
                    valid_type=ticket["valid_type"],
                )
            )

        for genre in night["genres"]:
            existing_genre = session.scalar(select(Genres).where(Genres.name == genre["name"]))
            if existing_genre is None:
                objects.append(
                    Genres(
                        ra_id=str(genre["ra_id"]),
                        night_id=night_id,
                        name=genre["name"],
                    )
                )

    if objects:
        session.add_all(objects)
