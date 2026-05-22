"""SQLAlchemy 2.0 declarative models.

All models use the new ``Mapped[...]`` / ``mapped_column`` API so types are
checked at the declaration site and the legacy ``Query`` API is no longer the
default.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Nights(Base):
    __tablename__ = "nights"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ra_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)
    content: Mapped[str | None] = mapped_column(nullable=True)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)

    images: Mapped[list[NightImages]] = relationship(
        back_populates="night", cascade="all, delete-orphan"
    )
    venue: Mapped[Venues | None] = relationship(
        back_populates="night", uselist=False, cascade="all, delete-orphan"
    )
    tickets: Mapped[list[Tickets]] = relationship(
        back_populates="night", cascade="all, delete-orphan"
    )
    promoters: Mapped[list[Promoters]] = relationship(
        back_populates="night", cascade="all, delete-orphan"
    )
    artists: Mapped[list[Artists]] = relationship(
        back_populates="night", cascade="all, delete-orphan"
    )
    genres: Mapped[list[Genres]] = relationship(
        back_populates="night", cascade="all, delete-orphan"
    )


class NightImages(Base):
    __tablename__ = "night_images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    night_id: Mapped[int] = mapped_column(ForeignKey("nights.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)

    night: Mapped[Nights] = relationship(back_populates="images")


class Countries(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ra_id: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    url_code: Mapped[str] = mapped_column(nullable=False)


class Areas(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ra_id: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), nullable=False)


class Venues(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ra_id: Mapped[str] = mapped_column(nullable=False)
    night_id: Mapped[int] = mapped_column(ForeignKey("nights.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str | None] = mapped_column(nullable=True)

    night: Mapped[Nights] = relationship(back_populates="venue")


class Tickets(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    night_id: Mapped[int] = mapped_column(ForeignKey("nights.id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    on_sale_from: Mapped[datetime | None] = mapped_column(nullable=True)
    valid_type: Mapped[str] = mapped_column(nullable=False)

    night: Mapped[Nights] = relationship(back_populates="tickets")


class Promoters(Base):
    __tablename__ = "promoters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ra_id: Mapped[str] = mapped_column(nullable=False)
    night_id: Mapped[int] = mapped_column(ForeignKey("nights.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    night: Mapped[Nights] = relationship(back_populates="promoters")


class Artists(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ra_id: Mapped[str] = mapped_column(nullable=False)
    night_id: Mapped[int] = mapped_column(ForeignKey("nights.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    night: Mapped[Nights] = relationship(back_populates="artists")


class Genres(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ra_id: Mapped[str | None] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    night_id: Mapped[int | None] = mapped_column(ForeignKey("nights.id"), nullable=True)

    night: Mapped[Nights | None] = relationship(back_populates="genres")
