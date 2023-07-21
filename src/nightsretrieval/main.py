from datetime import datetime

from database.operations import (
    create_tables,
    insert_nights_data,
    insert_night_images_data,
    insert_venues_data,
    insert_artists_data,
    insert_tickets_data,
    insert_promoters_data,
    insert_genres_data,
)
from nightsretrieval.json_parser import full_event_from_json, nights_ids_from_json
from nightsretrieval.ra import get_event, get_event_listings


def main():
    create_tables()
    events_ids = nights_ids_from_json(get_event_listings())

    events_json = []
    for event_id in events_ids:
        event_json = get_event(event_id)["data"]["event"]
        events_json.append(event_json)

    full_events = [full_event_from_json(event_json) for event_json in events_json]

    insert_nights_data(full_events)
    insert_night_images_data(full_events)
    insert_venues_data(full_events)
    insert_artists_data(full_events)
    insert_tickets_data(full_events)
    insert_promoters_data(full_events)
    insert_genres_data(full_events)
