from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # Firebase UID is the primary key
    name = Column(String, nullable=True)  # Pulled from Firebase on first login
    email = Column(String, unique=True, index=True, nullable=False)  # Pulled from Firebase on first login
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One user can have many cart items
    cart_items = relationship("Cart", back_populates="user")
    # One user can place many orders
    orders = relationship("Order", back_populates="user")
