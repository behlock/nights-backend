from datetime import datetime, timedelta

from database.operations import drop_tables, create_tables, insert_nights_data

from nightsretrieval.json_parser import full_event_from_json, nights_ids_from_json
from nightsretrieval.ra import get_event, get_event_listings
from utils.datetime_ex import datetime_to_str

AREA_ID = 13  # London

LISTING_DATE_LOWER_BOUND = datetime.now()
LISTING_DATE_UPPER_BOUND = datetime.now() + timedelta(days=10)


def main() -> None:
    drop_tables()
    create_tables()
    listings = get_event_listings(AREA_ID, LISTING_DATE_LOWER_BOUND, LISTING_DATE_UPPER_BOUND)
    events_ids = nights_ids_from_json(listings)

    events_json = []
    for event_id in events_ids:
        event_json = get_event(event_id)["data"]["event"]
        events_json.append(event_json)

    full_events = [full_event_from_json(event_json) for event_json in events_json]

    insert_nights_data(full_events)
