from datetime import timedelta, datetime
from typing import List

import httpx
from httpx import AsyncClient
from schemas import Flight, FlightPath, Journey


async def fetch_flights() -> List[Flight]:
    url = "https://mock.apidog.com/m1/814105-793312-default/flight-events"
    async with AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return [Flight(**flight) for flight in response.json()]


MAX_CONNECTIONS = 2
MAX_JOURNEY_DURATION = timedelta(hours=24)
MAX_CONNECTION_TIME = timedelta(hours=4)
FLIGHT_EVENTS_URL = "https://mock.apidog.com/m1/814105-793312-default/flight-events"


async def get_available_flights() -> List[Flight]:
    async with httpx.AsyncClient() as client:
        response = await client.get(FLIGHT_EVENTS_URL)
        response.raise_for_status()
        flights_data = response.json()
        return [Flight(**flight) for flight in flights_data]


async def search_journeys(from_: str, to: str, date: str) -> List[Journey]:
    all_flights = await get_available_flights()
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    matching_journeys: List[Journey] = []

    for flight1 in all_flights:
        if (
                flight1.departure_city != from_
                or flight1.departure_datetime.date() != date_obj.date()
        ):
            continue

        if flight1.arrival_city == to:
            matching_journeys.append(
                Journey(
                    connections=0,
                    path=[FlightPath.from_flight(flight1)]
                )
            )
            continue

        for flight2 in all_flights:
            if (
                    flight1.arrival_city != flight2.departure_city
                    or flight2.arrival_city != to
                    or flight1.arrival_city == to
                    or flight1 == flight2
            ):
                continue

            wait_time = flight2.departure_datetime - flight1.arrival_datetime
            total_duration = flight2.arrival_datetime - flight1.departure_datetime

            if (
                    timedelta() <= wait_time <= MAX_CONNECTION_TIME
                    and total_duration <= MAX_JOURNEY_DURATION
            ):
                matching_journeys.append(
                    Journey(
                        connections=1,
                        path=[
                            FlightPath.from_flight(flight1),
                            FlightPath.from_flight(flight2),
                        ],
                    )
                )

    return matching_journeys
