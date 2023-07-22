from datetime import datetime
from typing import Any, Optional
from nightsretrieval.graphql import send_graphql_request
from utils.datetime_ex import datetime_to_str


RA_API_URL = "https://ra.co/graphql"


# * Hardcoded to London for now
def get_event_listings(
    area_id: int = 13,
    number_of_events: int = 20,
    listing_date: Optional[str] = datetime_to_str(datetime.now()),
) -> Any:
    query = """
        query GET_EVENT_LISTINGS(
        $filters: FilterInputDtoInput
        $filterOptions: FilterOptionsInputDtoInput
        $page: Int
        $pageSize: Int
        ) {
        eventListings(
            filters: $filters
            filterOptions: $filterOptions
            pageSize: $pageSize
            page: $page
        ) {
            data {
            id
            listingDate
            event {
                ...eventListingsFields
                artists {
                id
                name
                __typename
                }
                __typename
            }
            __typename
            }
            filterOptions {
            genre {
                label
                value
                __typename
            }
            __typename
            }
            totalResults
            __typename
        }
        }

        fragment eventListingsFields on Event {
        id
        date
        startTime
        endTime
        title
        contentUrl
        flyerFront
        isTicketed
        attending
        queueItEnabled
        newEventForm
        images {
            id
            filename
            alt
            type
            crop
            __typename
        }
        pick {
            id
            blurb
            __typename
        }
        venue {
            id
            name
            contentUrl
            live
            __typename
        }
        __typename
        }
        """

    variables = {
        "filters": {"areas": {"eq": area_id}, "listingDate": {"gte": listing_date}},
        "filterOptions": {"genre": True},
        # "pageSize": number_of_events,
        # "page": 1,
    }

    payload = {"query": query, "variables": variables}
    data = send_graphql_request(api_url=RA_API_URL, payload=payload)
    return data


def get_event(event_id: int) -> Any:
    query = """
    query GET_EVENT($id: ID!, $isAuthenticated: Boolean!) {
  event(id: $id) {
    id
    title
    flyerFront
    flyerBack
    content
    minimumAge
    cost
    contentUrl
    embargoDate
    date
    time
    startTime
    endTime
    attending
    lineup
    isInterested
    isTicketed
    isFestival
    dateUpdated
    resaleActive
    newEventForm
    datePosted
    hasSecretVenue
    live
    canSubscribeToTicketNotifications
    images {
      id
      filename
      alt
      type
      crop
      __typename
    }
    venue {
      id
      name
      address
      contentUrl
      live
      area {
        id
        name
        urlName
        country {
          id
          name
          urlCode
          isoCode
          __typename
        }
        __typename
      }
      __typename
    }
    promoters {
      id
      name
      contentUrl
      live
      hasTicketAccess
      tracking(types: [PAGEVIEW]) {
        id
        code
        event
        __typename
      }
      __typename
    }
    artists {
      id
      name
      contentUrl
      urlSafeName
      __typename
    }
    pick {
      id
      blurb
      author {
        id
        name
        imageUrl
        username
        contributor
        __typename
      }
      __typename
    }
    promotionalLinks {
      title
      url
      __typename
    }
    tracking(types: [PAGEVIEW]) {
      id
      code
      event
      __typename
    }
    admin {
      id
      username
      __typename
    }
    tickets(queryType: AVAILABLE) {
      id
      title
      validType
      onSaleFrom
      priceRetail
      currency {
        id
        code
        __typename
      }
      __typename
    }
    standardTickets: tickets(queryType: AVAILABLE, ticketTierType: TICKETS) {
      id
      validType
      __typename
    }
    userOrders @include(if: $isAuthenticated) {
      id
      rAOrderNumber
      __typename
    }
    playerLinks {
      id
      sourceId
      audioService {
        id
        name
        __typename
      }
      __typename
    }
    childEvents {
      id
      date
      isTicketed
      __typename
    }
    genres {
      id
      name
      slug
      __typename
    }
    __typename
  }
}
        """

    variables = {
        "id": event_id,
        "isAuthenticated": False,
    }

    payload = {"query": query, "variables": variables}
    data = send_graphql_request(api_url=RA_API_URL, payload=payload)
    return data
