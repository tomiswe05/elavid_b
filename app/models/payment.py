from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)  # unique=True enforces one payment per order
    payment_ref = Column(String, nullable=True)  # Reference from payment provider (e.g. Paystack, Stripe)
    stripe_session_id = Column(String, nullable=True, unique=True)  # Stripe Checkout Session ID
    status = Column(String, default="pending")  # pending, success, failed
    provider = Column(String, nullable=True)  # Which payment gateway was used

    order = relationship("Order", back_populates="payment")
