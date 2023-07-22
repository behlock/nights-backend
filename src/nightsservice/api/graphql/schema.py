from graphene import ObjectType, String, NonNull, BigInt, DateTime, Field

from nightsservice.api.graphql.types import non_null_list_of


class NightImage(ObjectType):  # type: ignore
    night_image_id = NonNull(BigInt, description="Unique identifier for night image")
    url = NonNull(String, description="Resident Advisor URL of image")


class Country(ObjectType):  # type: ignore
    country_id = NonNull(BigInt, description="Unique identifier for country")
    ra_id = NonNull(BigInt, description="Resident Advisor ID")
    name = NonNull(String, description="Name of country")
    url_code = NonNull(String, description="Resident Advisor URL code of country")


class Area(ObjectType):  # type: ignore
    area_id = NonNull(BigInt, description="Unique identifier for area")
    ra_id = NonNull(BigInt, description="Resident Advisor ID")
    name = NonNull(String, description="Name of area")
    country = NonNull(Country, description="Country of area")


class Venue(ObjectType):  # type: ignore
    venue_id = NonNull(BigInt, description="Unique identifier for venue")
    ra_id = NonNull(BigInt, description="Resident Advisor ID")
    name = NonNull(String, description="Name of venue")
    address = Field(String, description="Address of venue")
    area = Field(Area, description="Area of venue")


class Ticket(ObjectType):  # type: ignore
    ticket_id = NonNull(BigInt, description="Unique identifier for ticket")
    title = NonNull(String, description="Title of ticket")
    price = NonNull(String, description="Price of ticket")
    on_sale_from = Field(DateTime, description="Date ticket goes on sale")
    valid_type = NonNull(String, description="Type of ticket")


class Promoter(ObjectType):  # type: ignore
    promoter_id = NonNull(BigInt, description="Unique identifier for promoter")
    ra_id = NonNull(BigInt, description="Resident Advisor ID")
    name = NonNull(String, description="Name of promoter")


class Artist(ObjectType):  # type: ignore
    artist_id = NonNull(BigInt, description="Unique identifier for artist")
    ra_id = NonNull(BigInt, description="Resident Advisor ID")
    name = NonNull(String, description="Name of artist")


class Night(ObjectType):  # type: ignore
    night_id = NonNull(BigInt, description="Unique identifier for night")
    ra_id = NonNull(BigInt, description="Resident Advisor ID")
    title = NonNull(String, description="Title of event")
    date = NonNull(DateTime, description="Date of event")
    content = Field(String, description="Description of event")
    start_time = NonNull(DateTime, description="Start time of event")
    end_time = NonNull(DateTime, description="End time of event")
    images = non_null_list_of(NightImage, description="Images of event")
    # venue = NonNull(Venue, description="Venue of event")
    venue = Field(Venue, description="Venue of event")
    tickets = non_null_list_of(Ticket, description="Tickets of event")
    promoters = non_null_list_of(Promoter, description="Promoters of event")
    artists = non_null_list_of(Artist, description="Artists of event")
