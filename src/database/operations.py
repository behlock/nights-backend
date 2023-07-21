from sqlalchemy.orm import Session

from database.model import Base, Nights
from database.connection import init_engine


def create_tables() -> None:
    engine = init_engine()
    Base.metadata.create_all(engine)


def insert_nights_data(nights):
    engine = init_engine()
    s = Session(engine)

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
    s.bulk_save_objects(objects)
    s.commit()
