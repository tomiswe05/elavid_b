from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)  # Firebase UID
    total_amount = Column(Float, nullable=False)  # Sum of all order items
    status = Column(String, default="pending")  # pending, paid, delivered
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="orders")
    # One order contains many order items
    order_items = relationship("OrderItem", back_populates="order")
    # One order has exactly one payment (uselist=False enforces one-to-one)
    payment = relationship("Payment", back_populates="order", uselist=False)
