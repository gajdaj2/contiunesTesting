# app.py – prosta aplikacja FastAPI z endpointem zamówień

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency – sesja bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemat wejściowy (Pydantic)
class OrderCreate(BaseModel):
    product: str
    quantity: int
    price: float

# POST /orders – tworzy nowe zamówienie
@app.post("/orders", status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    if order.quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be positive")
    if order.price <= 0:
        raise HTTPException(status_code=422, detail="Price must be positive")
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# GET /orders/{id} – zwraca zamówienie
@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order