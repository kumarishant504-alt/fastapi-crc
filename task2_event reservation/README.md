# Campus Event Seat Reservation API

## 1. Project Description
A FastAPI REST API that manages campus events (workshops, hackathons, seminars) and student seat reservations, preventing overbooking and reservations on closed events. All data is persisted in a SQLite database using SQLModel.

## 2. Technologies Used
- FastAPI
- SQLModel (Pydantic + SQLAlchemy)
- SQLite
- Uvicorn (ASGI server)

## 3. Installation Steps
```bash
git clone <your-repo-url>
cd <repo-folder>

python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## 4. Command to Run the FastAPI Application
```bash
uvicorn main:app --reload
```
The database file `event_reservation.db` and its tables (`event`, `reservation`) are created automatically on startup.

## 5. Swagger UI URL
```
http://127.0.0.1:8000/docs
```

## 6. Available Endpoints

### Events
| Method | Endpoint              | Description             |
|--------|------------------------|---------------------------|
| POST   | `/events`              | Create a new event        |
| GET    | `/events`              | Get all events             |
| GET    | `/events/{event_id}`   | Get a specific event       |
| PUT    | `/events/{event_id}`   | Update event information   |
| DELETE | `/events/{event_id}`   | Delete an event            |

### Reservations
| Method | Endpoint                              | Description                                 |
|--------|-----------------------------------------|-----------------------------------------------|
| POST   | `/events/{event_id}/reserve`           | Reserve a seat for an event                   |
| GET    | `/events/{event_id}/reservations`      | Get all reservations for an event             |
| DELETE | `/reservations/{reservation_id}`       | Cancel a reservation                          |
| GET    | `/events/{event_id}/availability`      | Get total/booked/remaining seats              |

### Business Logic
- A reservation is only accepted if: the event exists, the event's status is `Open`, and current reservations < `capacity`.
- Once an event reaches its `capacity`, further reservation requests return `400 Bad Request`.
- Reservations on a `Closed` event also return `400 Bad Request`.
- `capacity` must be greater than 0 (validated by SQLModel/Pydantic, returns `422` otherwise).
- `email` is validated as a proper email address (returns `422` if invalid).
- Requesting a non-existent event/reservation ID returns `404 Not Found`.

## Project Structure
```
.
├── main.py            # FastAPI app and routes
├── models.py           # Event, Reservation SQLModel models + schemas
├── database.py          # Engine (create_engine) and session setup
├── requirements.txt
├── README.md
└── screenshots/         # Proof-of-work screenshots (add your own)
```
