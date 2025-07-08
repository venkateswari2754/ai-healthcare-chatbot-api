
from pydantic import BaseModel
from datetime import datetime

class CreateOrder(BaseModel):
    user_id: int
    equipment_id: int
    status_id: int
    
class OrderOut(BaseModel):
    order_id: int
    user_id: int
    equipment_name: str
    status_id: int
    estimated_delivery_date: datetime  # Use appropriate type for date
    tracking_number: str
    ordered_at: datetime  # Use appropriate type for timestamp

    class Config:
        orm_mode = True