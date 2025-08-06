from datetime import datetime
from pydantic import BaseModel


class Flight(BaseModel):
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_datetime: datetime
    arrival_datetime: datetime


class FlightPath(BaseModel):
    flight_number: str
    from_: str
    to: str
    departure_time: datetime
    arrival_time: datetime

    model_config = {
        "populate_by_name": True,
        "validate_by_name": True
    }

    @classmethod
    def from_flight(cls, flight: Flight) -> "FlightPath":
        return cls(
            flight_number=flight.flight_number,
            from_=flight.departure_city,
            to=flight.arrival_city,
            departure_time=flight.departure_datetime,
            arrival_time=flight.arrival_datetime
        )


class Journey(BaseModel):
    connections: int
    path: list[FlightPath]
