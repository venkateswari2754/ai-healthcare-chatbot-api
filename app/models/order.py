from sqlalchemy import Column, Integer, String, ForeignKey,TIMESTAMP
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    equipment_name = Column(String, nullable=False)
    status_id = Column(Integer, nullable=False)
    estimated_delivery_date = Column(TIMESTAMP)
    tracking_number = Column(String, nullable=False)  # e.g., pending, completed, cancelled
    ordered_at =Column(TIMESTAMP)  # Use appropriate type for timestamp
   
