from typing import List

from fastapi import FastAPI, HTTPException, Depends, status as http_status
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Item, ItemCreate, ItemRead, ItemUpdate, StatusEnum

app = FastAPI(
    title="Campus Lost & Found API",
    description="A digital Lost & Found system for reporting and tracking lost/found items on campus.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """Create the SQLite database and tables when the app starts."""
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Campus Lost & Found API is running. Visit /docs for Swagger UI."}


# ---------- CREATE ----------
@app.post("/items", response_model=ItemRead, status_code=http_status.HTTP_201_CREATED)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# ---------- READ ALL ----------
@app.get("/items", response_model=List[ItemRead])
def get_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items


# ---------- READ ONE ----------
@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return item


# ---------- UPDATE ----------
@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item_update: ItemUpdate, session: Session = Depends(get_session)):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")

    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# ---------- DELETE ----------
@app.delete("/items/{item_id}", status_code=http_status.HTTP_200_OK)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    session.delete(db_item)
    session.commit()
    return {"message": f"Item with id {item_id} deleted successfully"}


# ---------- FILTER BY STATUS ----------
@app.get("/items/status/{item_status}", response_model=List[ItemRead])
def get_items_by_status(item_status: StatusEnum, session: Session = Depends(get_session)):
    items = session.exec(select(Item).where(Item.status == item_status)).all()
    return items


# ---------- FILTER BY CATEGORY ----------
@app.get("/items/category/{category}", response_model=List[ItemRead])
def get_items_by_category(category: str, session: Session = Depends(get_session)):
    items = session.exec(select(Item).where(Item.category == category)).all()
    return items