from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.schemas.order import CreateOrder, OrderOut
from app.database import SessionLocal
from app.crud import order as crud_order
from app.core import security
from app.database import get_db
from app.core.security import get_current_user

router= APIRouter()
@router.post("/order",response_model=OrderOut)
def create_order(create_order: CreateOrder, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    
    existing_order = crud_order.get_order_by_id(db, create_order.order_id)
    if existing_order:
        raise HTTPException(status_code=400, detail="Order already exists")
    
    order = crud_order.create_order(db, create_order,user_email=current_user)
    return order

@router.get("/orders")
def get_orders(current_user: str = Depends(get_current_user)):
    db: Session = Depends(get_db)
    orders = crud_order.get_orders_by_user_id(db, current_user.user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders
    