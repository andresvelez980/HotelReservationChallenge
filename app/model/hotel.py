from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import ClassVar

from app.services.util import (generate_unique_id, date_lower_than_today_error,
    reservation_not_found_error, guest_not_found_error, room_not_available_error,
    room_not_found_error, room_already_exists_error)


from dataclasses import dataclass

@dataclass
class Guest:
    REGULAR = "regular"
    VIP = "vip"

    name: str
    email: str
    type_: str = REGULAR

    def __str__(self) -> str:
        return f"Guest {self.name} ({self.email}) of type {self.type_}"


@dataclass
class Reservation:
    guest_name: str
    description: str
    check_in: date
    check_out: date

    guests: list[Guest] = field(default_factory=list)
    id: str = field(default_factory=generate_unique_id)

    def add_guest(self, name: str, email: str, type_: str):
        guest = Guest(name, email, type_)
        self.guests.append(guest)

    def delete_guest(self, guest_index: int):
        if 0 <= guest_index < len(self.guests):
            self.guests.pop(guest_index)
        else:
            guest_not_found_error()

    def __len__(self) -> int:
        return (self.check_out - self.check_in).days

    def __str__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"Guest: {self.guest_name}\n"
            f"Description: {self.description}\n"
            f"Dates: {self.check_in} - {self.check_out}"
        )


class Room:
    def __init__(self, number: int, type_: str, price_per_night: float):
        self.number = number
        self.type_ = type_
        self.price_per_night = price_per_night
        self.availability: dict = {}

        self._init_availability()

    def _init_availability(self):
        today = datetime.now().date()
        for i in range(365):
            self.availability[today + timedelta(days=i)] = None

    def book(self, reservation_id: str, check_in, check_out):
        current = check_in

        while current < check_out:
            if self.availability.get(current) is not None:
                room_not_available_error()
            current += timedelta(days=1)

        current = check_in
        while current < check_out:
            self.availability[current] = reservation_id
            current += timedelta(days=1)

    def release(self, reservation_id: str):
        released = False
        for d, saved_id in self.availability.items():
            if saved_id == reservation_id:
                self.availability[d] = None
                released = True
        if not released:
            reservation_not_found_error()

    def update_booking(self, reservation_id: str, check_in, check_out):
        for d in self.availability:
            if self.availability[d] == reservation_id:
                self.availability[d] = None

        current = check_in
        while current < check_out:
            if self.availability.get(current) is not None:
                room_not_available_error()
            else:
                self.availability[current] = reservation_id
            current += timedelta(days=1)


# TODO: Implement Hotel class here
