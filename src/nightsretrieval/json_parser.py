from utils.datetime import str_to_datetime


def nights_ids_from_json(nights_json):
    nights_ids = []
    for night in nights_json["data"]["eventListings"]["data"]:
        nights_ids.append(night["event"]["id"])

    return nights_ids


def night_from_json(night_json):
    return {
        "ra_id": int(night_json["id"]),
        "title": night_json["title"],
        "content": night_json["content"],
        "date": str_to_datetime(night_json["date"]),
        "start_time": str_to_datetime(night_json["startTime"]),
        "end_time": str_to_datetime(night_json["endTime"]),
        "images": [image["filename"] for image in night_json["images"]],
        "venue": {
            "ra_id": int(night_json["venue"]["id"]),
            "name": night_json["venue"]["name"],
            "address": night_json["venue"]["address"],
            "area": {
                "ra_id": night_json["venue"]["area"]["id"],
                "name": night_json["venue"]["area"]["name"],
                "country": {
                    "ra_id": night_json["venue"]["area"]["country"]["id"],
                    "name": night_json["venue"]["area"]["country"]["name"],
                    "url_code": night_json["venue"]["area"]["country"]["urlCode"],
                },
            },
        },
        "promoters": [
            {"ra_id": int(promoter["id"]), "name": promoter["name"]}
            for promoter in night_json["promoters"]
        ],
        "artists": [
            {"ra_id": int(artist["id"]), "name": artist["name"]}
            for artist in night_json["artists"]
        ],
        "tickets": [
            {
                "ra_id": int(ticket["id"]),
                "title": ticket["title"],
                "price": ticket["priceRetail"],
                "on_sale_from": ticket["onSaleFrom"],
                "valid_type": ticket["validType"],
            }
            for ticket in night_json["tickets"]
        ],
        "genres": [
            {"ra_id": int(genre["id"]), "name": genre["name"]} for genre in night_json["genres"]
        ],
    }
