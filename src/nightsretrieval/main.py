from datetime import datetime

from database.operations import create_tables, insert_nights_data
from nightsretrieval.json_parser import night_from_json, nights_ids_from_json
from nightsretrieval.ra import get_event, get_event_listings


def main():
    create_tables()
    events_ids = nights_ids_from_json(get_event_listings())

    events_json = []
    for event_id in events_ids:
        event_json = get_event(event_id)["data"]["event"]
        events_json.append(event_json)

    events = [night_from_json(event_json) for event_json in events_json]

    insert_nights_data(events)
