from typing import List

from fastapi import FastAPI, HTTPException, Depends, status as http_status
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import (
    Event, EventCreate, EventRead, EventUpdate, EventStatusEnum,
    Reservation, ReservationCreate, ReservationRead,
    AvailabilityRead,
)

app = FastAPI(
    title="Campus Event Seat Reservation API",
    description="Manages campus events (workshops, hackathons, seminars) and student seat reservations.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Campus Event Seat Reservation API is running. Visit /docs for Swagger UI."}


# =====================================================
# EVENT ROUTES
# =====================================================

@app.post("/events", response_model=EventRead, status_code=http_status.HTTP_201_CREATED)
def create_event(event: EventCreate, session: Session = Depends(get_session)):
    db_event = Event.model_validate(event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@app.get("/events", response_model=List[EventRead])
def get_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()


@app.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
    return event


@app.put("/events/{event_id}", response_model=EventRead)
def update_event(event_id: int, event_update: EventUpdate, session: Session = Depends(get_session)):
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")

    update_data = event_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@app.delete("/events/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_session)):
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
    session.delete(db_event)
    session.commit()
    return {"message": f"Event with id {event_id} deleted successfully"}


# =====================================================
# RESERVATION ROUTES
# =====================================================

@app.post("/events/{event_id}/reserve", response_model=ReservationRead, status_code=http_status.HTTP_201_CREATED)
def create_reservation(event_id: int, reservation: ReservationCreate, session: Session = Depends(get_session)):
    # 1. Verify event exists
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")

    # 2. Verify event is Open
    if event.status != EventStatusEnum.Open:
        raise HTTPException(status_code=400, detail="Cannot reserve a seat: event is Closed")

    # 3. Check existing reservation count vs capacity
    existing_count = len(
        session.exec(select(Reservation).where(Reservation.event_id == event_id)).all()
    )
    if existing_count >= event.capacity:
        raise HTTPException(status_code=400, detail="Cannot reserve a seat: event is already full")

    # 4. Create reservation
    db_reservation = Reservation.model_validate(reservation, update={"event_id": event_id})
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation


@app.get("/events/{event_id}/reservations", response_model=List[ReservationRead])
def get_event_reservations(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
    return session.exec(select(Reservation).where(Reservation.event_id == event_id)).all()


@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail=f"Reservation with id {reservation_id} not found")
    session.delete(reservation)
    session.commit()
    return {"message": f"Reservation with id {reservation_id} cancelled successfully"}


@app.get("/events/{event_id}/availability", response_model=AvailabilityRead)
def get_event_availability(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")

    booked = len(
        session.exec(select(Reservation).where(Reservation.event_id == event_id)).all()
    )
    remaining = event.capacity - booked
    return AvailabilityRead(capacity=event.capacity, booked=booked, remaining=remaining)
