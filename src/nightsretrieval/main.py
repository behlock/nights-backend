from datetime import datetime

from database.operations import create_tables, insert_nights_data

from nightsretrieval.json_parser import full_event_from_json, nights_ids_from_json
from nightsretrieval.ra import get_event, get_event_listings
from utils.datetime_ex import datetime_to_str

AREA_ID = 13  # London
NUMBER_OF_EVENTS = 50
LISTING_DATE = datetime_to_str(datetime.now())


def main() -> None:
    create_tables()
    listings = get_event_listings(AREA_ID, NUMBER_OF_EVENTS, LISTING_DATE)
    events_ids = nights_ids_from_json(listings)

    events_json = []
    for event_id in events_ids:
        event_json = get_event(event_id)["data"]["event"]
        events_json.append(event_json)

    full_events = [full_event_from_json(event_json) for event_json in events_json]

    insert_nights_data(full_events)
