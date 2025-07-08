from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import CreateOrder

def create_order(db: Session, order: CreateOrder) -> Order:
    db_order= Order(
        user_id=order.user_id,
        equipment_id=order.equipment_id,
        status_id=order.status_id,
        estimated_delivery_date=order.estimated_delivery_date,
        tracking_number=order.tracking_number,
        ordered_at=order.ordered_at
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.order_id == order_id).first()

def get_orders_by_user_id(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()
def get_all_orders(db: Session):
    return db.query(Order).all()

def update_order_status(db: Session, order_id: int, status_id: int) -> Order | None:
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        order.status_id = status_id
        db.commit()
        db.refresh(order)
        return order
    return None

def delete_order(db: Session, order_id: int) -> bool:
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
        return True
    return False