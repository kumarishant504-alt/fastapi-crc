# Campus Lost & Found API

## 1. Project Description
A FastAPI REST API that lets students report lost or found items on campus, track their status (Lost / Found / Returned), and search items by status or category. All data is persisted in a SQLite database using SQLModel.

## 2. Technologies Used
- FastAPI
- SQLModel (Pydantic + SQLAlchemy)
- SQLite
- Uvicorn (ASGI server)

## 3. Installation Steps
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 4. Command to Run the FastAPI Application
```bash
uvicorn main:app --reload
```
The database file `lost_and_found.db` and its tables are created automatically on startup.

## 5. Swagger UI URL
Once the server is running, open:
```
http://127.0.0.1:8000/docs
```
(Alternative ReDoc UI: `http://127.0.0.1:8000/redoc`)

## 6. Available Endpoints

| Method | Endpoint                        | Description                              |
|--------|----------------------------------|-------------------------------------------|
| POST   | `/items`                        | Create a new lost/found item              |
| GET    | `/items`                        | Get all reported items                    |
| GET    | `/items/{item_id}`              | Get a specific item by ID                 |
| PUT    | `/items/{item_id}`              | Update an item's details/status           |
| DELETE | `/items/{item_id}`              | Delete an item report                     |
| GET    | `/items/status/{status}`        | Get items filtered by status (Lost/Found/Returned) |
| GET    | `/items/category/{category}`    | Get items filtered by category            |

### Item fields
`id`, `title`, `description`, `category`, `location`, `reported_by`, `status` (`Lost` / `Found` / `Returned`)

### Validation
- `title` and `description` cannot be empty.
- `status` only accepts `Lost`, `Found`, or `Returned` (invalid values return `422 Unprocessable Entity`).
- Requesting a non-existent item ID returns `404 Not Found`.

## Project Structure
```
.
├── main.py            # FastAPI app and routes
├── models.py           # SQLModel Item model + Pydantic schemas
├── database.py          # Engine (create_engine) and session setup
├── requirements.txt
├── README.md
└── screenshots/         # Proof-of-work screenshots (add your own)
```