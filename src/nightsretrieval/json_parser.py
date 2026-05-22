from __future__ import annotations

from typing import Any

import structlog

from nightsretrieval.utils.datetime_ex import str_to_datetime

logger = structlog.get_logger(__name__)


def nights_ids_from_json(nights_json: dict[str, Any] | None) -> list[int]:
    """Extract event ids from an RA event-listings response, defensively."""
    if not nights_json:
        logger.warning("ra_listings_empty_response")
        return []

    listings = (
        nights_json.get("data", {})
        .get("eventListings", {})
        .get("data", [])
        if isinstance(nights_json, dict)
        else []
    )
    if not isinstance(listings, list):
        logger.warning("ra_listings_unexpected_shape")
        return []

    ids: list[int] = []
    for night in listings:
        event = (night or {}).get("event") or {}
        event_id = event.get("id")
        if event_id is None:
            continue
        try:
            ids.append(int(event_id))
        except (TypeError, ValueError):
            logger.warning("ra_listings_unparseable_id", value=event_id)
    return ids


def full_event_from_json(night_json: dict[str, Any]) -> dict[str, Any]:
    venue = night_json.get("venue") or {}
    area = venue.get("area") or {}
    country = area.get("country") or {}

    return {
        "ra_id": int(night_json["id"]),
        "title": night_json.get("title", ""),
        "content": night_json.get("content"),
        "date": str_to_datetime(night_json.get("date")),
        "start_time": str_to_datetime(night_json.get("startTime")),
        "end_time": str_to_datetime(night_json.get("endTime")),
        "images": [
            image["filename"]
            for image in (night_json.get("images") or [])
            if image.get("filename")
        ],
        "venue": {
            "ra_id": int(venue["id"]) if venue.get("id") is not None else None,
            "name": venue.get("name"),
            "address": venue.get("address"),
            "area": {
                "ra_id": area.get("id"),
                "name": area.get("name"),
                "country": {
                    "ra_id": country.get("id"),
                    "name": country.get("name"),
                    "url_code": country.get("urlCode"),
                },
            },
        },
        "promoters": [
            {"ra_id": int(p["id"]), "name": p.get("name", "")}
            for p in (night_json.get("promoters") or [])
            if p.get("id") is not None
        ],
        "artists": [
            {"ra_id": int(a["id"]), "name": a.get("name", "")}
            for a in (night_json.get("artists") or [])
            if a.get("id") is not None
        ],
        "tickets": [
            {
                "ra_id": int(t["id"]),
                "title": t.get("title", ""),
                "price": str(t.get("priceRetail", "")),
                "on_sale_from": str_to_datetime(t.get("onSaleFrom")),
                "valid_type": t.get("validType", ""),
            }
            for t in (night_json.get("tickets") or [])
            if t.get("id") is not None
        ],
        "genres": [
            {"ra_id": int(g["id"]), "name": g.get("name", "")}
            for g in (night_json.get("genres") or [])
            if g.get("id") is not None
        ],
    }
