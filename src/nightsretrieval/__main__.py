from datetime import datetime, timedelta
import sys
from database.connection import init_engine

from database.operations import setup_tables, insert_nights_data

from nightsretrieval.json_parser import full_event_from_json, nights_ids_from_json
from nightsretrieval.ra import get_event, get_event_listings

AREA_ID = 13  # London

LISTING_DATE_LOWER_BOUND = datetime.now()
LISTING_DATE_UPPER_BOUND = datetime.now() + timedelta(days=10)


def main(is_local: bool) -> None:
    engine = init_engine(is_local)
    setup_tables(engine)
    listings = get_event_listings(AREA_ID, LISTING_DATE_LOWER_BOUND, LISTING_DATE_UPPER_BOUND)
    events_ids = nights_ids_from_json(listings)

    events_json = []
    for event_id in events_ids:
        event = get_event(event_id)
        if not event or not event["data"] or not event["data"]["event"]:
            continue

        event_json = get_event(event_id)["data"]["event"]
        events_json.append(event_json)

    full_events = [full_event_from_json(event_json) for event_json in events_json]

    insert_nights_data(engine, full_events)


if __name__ == "__main__":
    is_local = len(sys.argv) > 1 and bool(sys.argv[1]) is True
    main(is_local=is_local)
