from __future__ import annotations

from datetime import UTC, datetime, timedelta

import structlog
import typer

from database.connection import init_engine
from database.operations import insert_nights_data, setup_tables
from nightsretrieval.json_parser import full_event_from_json, nights_ids_from_json
from nightsretrieval.ra import get_event, get_event_listings
from nightsservice.logging_config import configure_logging
from nightsservice.settings import get_app_settings

app = typer.Typer(add_completion=False)


def _retrieve(is_local: bool, area_id: int, days_ahead: int) -> None:
    settings = get_app_settings()
    configure_logging(level=settings.LOG_LEVEL, is_production=settings.is_production)

    log = structlog.get_logger(__name__)
    log.info("nights_retrieval_started", is_local=is_local, area_id=area_id, days_ahead=days_ahead)

    engine = init_engine(is_local=is_local)
    setup_tables(engine)

    lower = datetime.now(UTC)
    upper = lower + timedelta(days=days_ahead)
    listings = get_event_listings(area_id, lower, upper)
    event_ids = nights_ids_from_json(listings)
    log.info("nights_retrieval_listings_fetched", count=len(event_ids))

    events_json: list[dict[str, object]] = []
    for event_id in event_ids:
        event = get_event(event_id)
        event_payload = (event or {}).get("data", {}).get("event")
        if not event_payload:
            log.warning("nights_retrieval_event_missing", event_id=event_id)
            continue
        events_json.append(event_payload)

    full_events = [full_event_from_json(event_json) for event_json in events_json]
    insert_nights_data(engine, full_events)
    log.info("nights_retrieval_completed", inserted=len(full_events))


@app.command()
def retrieve(
    is_local: bool = typer.Option(
        False, "--local/--prod", help="Write to local SQLite instead of Postgres."
    ),
    area_id: int = typer.Option(13, help="RA area id (13 = London)."),
    days_ahead: int = typer.Option(10, help="Number of days of upcoming events to fetch."),
) -> None:
    """Scrape upcoming RA events for an area and persist them."""
    _retrieve(is_local=is_local, area_id=area_id, days_ahead=days_ahead)


if __name__ == "__main__":
    app()
