from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class EventStatusEnum(str, Enum):
    Open = "Open"
    Closed = "Closed"


# ---------------- EVENT ----------------

class EventBase(SQLModel):
    title: str = Field(..., min_length=1)
    venue: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)  # capacity must be greater than 0
    organizer: str = Field(..., min_length=1)
    status: EventStatusEnum = EventStatusEnum.Open


class Event(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    title: Optional[str] = None
    venue: Optional[str] = None
    capacity: Optional[int] = Field(default=None, gt=0)
    organizer: Optional[str] = None
    status: Optional[EventStatusEnum] = None


class EventRead(EventBase):
    id: int


# ---------------- RESERVATION ----------------

class ReservationBase(SQLModel):
    student_name: str = Field(..., min_length=1)
    roll_number: str = Field(..., min_length=1)
    email: EmailStr


class Reservation(ReservationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")


class ReservationCreate(ReservationBase):
    """Body for POST /events/{event_id}/reserve (event_id comes from the URL path)"""
    pass


class ReservationRead(ReservationBase):
    id: int
    event_id: int


# ---------------- AVAILABILITY ----------------

class AvailabilityRead(SQLModel):
    capacity: int
    booked: int
    remaining: int
