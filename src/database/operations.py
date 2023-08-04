from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from database.model import (
    Base,
    Nights,
    NightImages,
    Countries,
    Venues,
    Tickets,
    Promoters,
    Artists,
    Genres,
)
from nightsservice.api.graphql.inputs import NightsInput
from nightsservice.api.graphql.schema import (
    Area,
    Country,
    Genre,
    Night,
    NightImage,
    Venue,
    Ticket,
    Promoter,
    Artist,
)


def insert_data(session: Session, objects: List[Any]) -> None:
    session.bulk_save_objects(objects)
    session.commit()


# TODO: Make db agnostic to the data it receives
def get_images_for_night(session: Session, night_id: int) -> List[NightImage]:
    db_images = session.query(NightImages).filter(NightImages.night_id == night_id).all()
    images = []
    for db_image in db_images:
        image = NightImage(
            night_image_id=db_image.id,
            url=db_image.image_url,
        )
        images.append(image)
    return images


def get_country_for_area(session: Session, country_id: int) -> Country:
    db_country = session.query(Countries).filter(Countries.id == country_id).first()
    country = Country(
        country_id=db_country.id,
        ra_id=db_country.ra_id,
        name=db_country.name,
        url_code=db_country.url_code,
    )
    return country


# TODO
def get_area_for_venue(session: Session, area_id: int) -> Area:
    # s = Session(init_engine())
    # db_area = session.query(Areas).filter(Areas.id == area_id).first()
    # area = Area(
    #     area_id=db_area.id,
    #     ra_id=db_area.ra_id,
    #     name=db_area.name,
    #     country=get_country_for_area(db_area.country_id),
    # )
    # return area

    return Area(
        area_id=1,
        ra_id=13,
        name="London",
        country=Country(
            country_id=1,
            ra_id=3,
            name="United Kingdom",
            url_code="UK",
        ),
    )


def get_venue_for_night(session: Session, night_id: int) -> Optional[Venue]:
    db_venue = session.query(Venues).filter(Venues.night_id == night_id).first()

    if db_venue is None:
        return None

    venue = Venue(
        venue_id=db_venue.id,
        ra_id=db_venue.ra_id,
        name=db_venue.name,
        address=db_venue.address,
        area=get_area_for_venue(session, db_venue.area_id),
    )
    return venue


def get_tickets_for_night(session: Session, night_id: int) -> List[Ticket]:
    db_tickets = session.query(Tickets).filter(Tickets.night_id == night_id).all()
    tickets = []
    for db_ticket in db_tickets:
        ticket = Ticket(
            ticket_id=db_ticket.id,
            title=db_ticket.title,
            price=db_ticket.price,
            on_sale_from=db_ticket.on_sale_from,
            valid_type=db_ticket.valid_type,
        )
        tickets.append(ticket)
    return tickets


def get_promoters_for_night(session: Session, night_id: int) -> List[Promoter]:
    db_promoters = session.query(Promoters).filter(Promoters.night_id == night_id).all()
    promoters = []
    for db_promoter in db_promoters:
        promoter = Promoter(
            promoter_id=db_promoter.id,
            ra_id=db_promoter.ra_id,
            name=db_promoter.name,
        )
        promoters.append(promoter)
    return promoters


def get_artists_for_night(session: Session, night_id: int) -> List[Artist]:
    db_artists = session.query(Artists).filter(Artists.night_id == night_id).all()
    artists = []
    for db_artist in db_artists:
        artist = Artist(
            artist_id=db_artist.id,
            ra_id=db_artist.ra_id,
            name=db_artist.name,
        )
        artists.append(artist)
    return artists


def get_genres_for_night(session: Session, night_id: int) -> List[Genre]:
    db_genres = session.query(Genres).filter(Genres.night_id == night_id).all()
    genres = []
    for db_genre in db_genres:
        genre = Genre(
            genre_id=db_genre.id,
            ra_id=db_genre.ra_id,
            name=db_genre.name,
        )
        genres.append(genre)
    return genres


def get_night_id_from_ra_id(session: Session, ra_id: int) -> int:
    db_night = session.query(Nights).filter(Nights.ra_id == ra_id).first()
    if db_night is None:
        raise Exception(f"Night with ra_id {ra_id} does not exist")

    return int(db_night.id)


def get_nights(engine: create_engine, input: Optional[NightsInput]) -> List[Night]:
    # TODO: use input
    session = Session(engine)
    db_nights = session.query(Nights).all()
    nights = []
    for db_night in db_nights:
        night = Night(
            night_id=db_night.id,
            ra_id=db_night.ra_id,
            title=db_night.title,
            date=db_night.date,
            content=db_night.content,
            start_time=db_night.start_time,
            end_time=db_night.end_time,
            images=get_images_for_night(session, db_night.id),
            venue=get_venue_for_night(session, db_night.id),
            tickets=get_tickets_for_night(session, db_night.id),
            promoters=get_promoters_for_night(session, db_night.id),
            artists=get_artists_for_night(session, db_night.id),
            genres=get_genres_for_night(session, db_night.id),
        )
        nights.append(night)
    return nights


def setup_tables(engine: create_engine) -> None:
    drop_tables(engine)
    create_tables(engine)


def drop_tables(engine: create_engine) -> None:
    Base.metadata.drop_all(engine)


def create_tables(engine: create_engine) -> None:
    Base.metadata.create_all(engine)


def insert_nights_data(engine: create_engine, nights: List[Dict[str, Any]]) -> None:
    session = Session(engine)
    insert_basic_nights_data(session, nights)
    insert_additional_nights_data(session, nights)


def insert_basic_nights_data(session: Session, nights: List[Dict[str, Any]]) -> None:
    objects = []
    for night in nights:
        if session.query(Nights).filter(Nights.ra_id == night["ra_id"]).first() is None:
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

    insert_data(session, objects)


def insert_additional_nights_data(session: Session, nights: List[Dict[str, Any]]) -> None:
    objects = []
    for night in nights:
        for image in night["images"]:
            if session.query(NightImages).filter(NightImages.image_url == image).first() is None:
                objects.append(
                    NightImages(
                        night_id=get_night_id_from_ra_id(session, night["ra_id"]),
                        image_url=image,
                    )
                )

        if session.query(Venues).filter(Venues.ra_id == night["venue"]["ra_id"]).first() is None:
            objects.append(
                Venues(
                    ra_id=night["venue"]["ra_id"],
                    night_id=get_night_id_from_ra_id(session, night["ra_id"]),
                    name=night["venue"]["name"],
                    address=night["venue"]["address"],
                    area_id=night["venue"]["area"]["ra_id"],
                )
            )

        for promoter in night["promoters"]:
            if (
                session.query(Promoters).filter(Promoters.ra_id == promoter["ra_id"]).first()
                is None
            ):
                objects.append(
                    Promoters(
                        ra_id=promoter["ra_id"],
                        night_id=get_night_id_from_ra_id(session, night["ra_id"]),
                        name=promoter["name"],
                    )
                )

        for artist in night["artists"]:
            if session.query(Artists).filter(Artists.ra_id == artist["ra_id"]).first() is None:
                objects.append(
                    Artists(
                        ra_id=artist["ra_id"],
                        night_id=get_night_id_from_ra_id(session, night["ra_id"]),
                        name=artist["name"],
                    )
                )

        for ticket in night["tickets"]:
            objects.append(
                Tickets(
                    night_id=get_night_id_from_ra_id(session, night["ra_id"]),
                    title=ticket["title"],
                    price=ticket["price"],
                    on_sale_from=ticket["on_sale_from"],
                    valid_type=ticket["valid_type"],
                )
            )

        for genre in night["genres"]:
            if session.query(Genres).filter(Genres.name == genre["name"]).first() is None:
                objects.append(
                    Genres(
                        night_id=get_night_id_from_ra_id(session, night["ra_id"]),
                        name=genre["name"],
                    )
                )

    insert_data(session, objects)
