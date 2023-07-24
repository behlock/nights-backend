import sqlalchemy as sqla
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Nights(Base):  # type: ignore
    __tablename__ = "nights"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    ra_id = sqla.Column(sqla.Integer, nullable=False, index=False)
    title = sqla.Column(sqla.String, nullable=False, index=False)
    date = sqla.Column(sqla.DateTime, nullable=False, index=False)
    content = sqla.Column(sqla.String, nullable=True, index=False)
    start_time = sqla.Column(sqla.DateTime, nullable=False, index=False)
    end_time = sqla.Column(sqla.DateTime, nullable=False, index=False)


class NightImages(Base):  # type: ignore
    __tablename__ = "night_images"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    night_id = sqla.Column(sqla.Integer, ForeignKey("nights.id"), nullable=False, index=False)
    image_url = sqla.Column(sqla.String, nullable=False, index=False)


class Countries(Base):  # type: ignore
    __tablename__ = "countries"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    ra_id = sqla.Column(sqla.String, nullable=False, index=False)
    name = sqla.Column(sqla.String, nullable=False, index=False)
    url_code = sqla.Column(sqla.String, nullable=False, index=False)


class Areas(Base):  # type: ignore
    __tablename__ = "areas"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    ra_id = sqla.Column(sqla.String, nullable=False, index=False)
    name = sqla.Column(sqla.String, nullable=False, index=False)
    country_id = sqla.Column(sqla.Integer, ForeignKey("countries.id"), nullable=False, index=False)


class Venues(Base):  # type: ignore
    __tablename__ = "venues"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    ra_id = sqla.Column(sqla.String, nullable=False, index=False)
    night_id = sqla.Column(sqla.Integer, ForeignKey("nights.id"), nullable=False, index=False)
    name = sqla.Column(sqla.String, nullable=False, index=False)
    address = sqla.Column(sqla.String, nullable=True, index=False)
    area_id = sqla.Column(sqla.Integer, ForeignKey("areas.id"), nullable=False, index=False)
    # website_url = sqla.Column(sqla.String, nullable=False, index=False)


class Tickets(Base):  # type: ignore
    __tablename__ = "tickets"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    night_id = sqla.Column(sqla.Integer, ForeignKey("nights.id"), nullable=False, index=False)
    title = sqla.Column(sqla.String, nullable=False, index=False)
    price = sqla.Column(sqla.String, nullable=False, index=False)
    on_sale_from = sqla.Column(sqla.DateTime, nullable=True, index=False)
    valid_type = sqla.Column(sqla.String, nullable=False, index=False)


class Promoters(Base):  # type: ignore
    __tablename__ = "promoters"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    ra_id = sqla.Column(sqla.String, nullable=False, index=False)
    night_id = sqla.Column(sqla.Integer, ForeignKey("nights.id"), nullable=False, index=False)
    name = sqla.Column(sqla.String, nullable=False, index=False)


class Artists(Base):  # type: ignore
    __tablename__ = "artists"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    ra_id = sqla.Column(sqla.String, nullable=False, index=False)
    night_id = sqla.Column(sqla.Integer, ForeignKey("nights.id"), nullable=False, index=False)
    name = sqla.Column(sqla.String, nullable=False, index=False)
    # TODO
    # spotify_id = sqla.Column(sqla.String, nullable=True, index=False)


class Genres(Base):  # type: ignore
    __tablename__ = "genres"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    ra_id = sqla.Column(sqla.String, nullable=True, index=False)
    name = sqla.Column(sqla.String, nullable=False, index=False)
    night_id = sqla.Column(sqla.Integer, ForeignKey("nights.id"), nullable=True, index=False)
    # TODO
    # artist_id = sqla.Column(sqla.Integer, ForeignKey("artists.id"), nullable=True, index=False)
