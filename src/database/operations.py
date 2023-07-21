from sqlalchemy.orm import Session

from database.model import (
    Base,
    Nights,
    NightImages,
    Countries,
    Areas,
    Venues,
    Tickets,
    Promoters,
    Artists,
    Genres,
)
from database.connection import init_engine


def insert_data(objects):
    s = Session(init_engine())
    s.bulk_save_objects(objects)
    s.commit()


def create_tables() -> None:
    engine = init_engine()
    Base.metadata.create_all(engine)


def insert_nights_data(nights):
    objects = [
        Nights(
            ra_id=night["ra_id"],
            title=night["title"],
            date=night["date"],
            content=night["content"],
            start_time=night["start_time"],
            end_time=night["end_time"],
        )
        for night in nights
    ]

    insert_data(objects)


def insert_night_images_data(nights):
    objects = []
    for night in nights:
        for image in night["images"]:
            objects.append(
                NightImages(
                    night_id=night["ra_id"],
                    image_url=image,
                )
            )

    insert_data(objects)

def insert_venues_data(nights):
    objects = []
    for night in nights:
        objects.append(
            Venues(
                ra_id=night["venue"]["ra_id"],
                night_id=night["ra_id"],
                name=night["venue"]["name"],
                address=night["venue"]["address"],
                area_id=night["venue"]["area"]["ra_id"],
            )
        )

    insert_data(objects)

def insert_promoters_data(nights):
    objects = []
    for night in nights:
        for promoter in night["promoters"]:
            objects.append(
                Promoters(
                    ra_id=promoter["ra_id"],
                    night_id=night["ra_id"],
                    name=promoter["name"],
                )
            )

    insert_data(objects)

def insert_artists_data(nights):
    objects = []
    for night in nights:
        for artist in night["artists"]:
            objects.append(
                Artists(
                    ra_id=artist["ra_id"],
                    night_id=night["ra_id"],
                    name=artist["name"],
                )
            )

    insert_data(objects)

def insert_tickets_data(nights):
    objects = []
    for night in nights:
        for ticket in night["tickets"]:
            objects.append(
                Tickets(
                    night_id=night["ra_id"],
                    title=ticket["title"],
                    price=ticket["price"],
                    on_sale_from=ticket["on_sale_from"],
                    valid_type=ticket["valid_type"],
                )
            )

    insert_data(objects)

def insert_genres_data(nights):
    objects = []
    for night in nights:
        for genre in night["genres"]:
            objects.append(
                Genres(
                    name=genre["name"],
                )
            )

    insert_data(objects)


