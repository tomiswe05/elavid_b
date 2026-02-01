from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment


class OrderService:

    # Create an order from snapshotted cart data (called after payment succeeds)
    def create_order_from_cart_data(
        db: Session,
        user_id: str,
        cart_snapshot: list,
        payment_ref: str,
        stripe_session_id: str
    ):
        # Calculate total amount from the snapshot
        total_amount = 0.0
        for item in cart_snapshot:
            total_amount += item["price"] * item["quantity"]

        # Create the order
        order = Order(
            user_id=user_id,
            total_amount=round(total_amount, 2),
            status="paid"
        )
        db.add(order)
        db.flush()  # Get order.id without committing

        # Create order items from the snapshot
        for item in cart_snapshot:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"]
            )
            db.add(order_item)

        # Create a payment record marked as success
        payment = Payment(
            order_id=order.id,
            payment_ref=payment_ref,
            stripe_session_id=stripe_session_id,
            status="success",
            provider="stripe"
        )
        db.add(payment)

        db.commit()
        db.refresh(order)
        return order

    # Get all orders for a user
    def get_user_orders(db: Session, user_id: str):
        return db.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.created_at.desc()).all()

    # Get a single order by ID (only if it belongs to the user)
    def get_order_by_id(db: Session, user_id: str, order_id: int):
        return db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
