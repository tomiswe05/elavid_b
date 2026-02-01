import os
import json
import stripe
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cart import Cart
from app.models.product import Product
from app.models.payment import Payment
from app.services.order_service import OrderService

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaymentService:

    # Create a Stripe Checkout Session from the user's cart
    def create_checkout_session(db: Session, user_id: str):
        # 1. Fetch cart items
        cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # 2. Validate stock and build line items
        line_items = []
        cart_snapshot = []

        for item in cart_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with id {item.product_id} not found"
                )
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for '{product.name}'. Available: {product.stock}, requested: {item.quantity}"
                )

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),  # Stripe expects cents
                },
                "quantity": item.quantity,
            })

            cart_snapshot.append({
                "product_id": product.id,
                "quantity": item.quantity,
                "price": product.price,
            })

        # 3. Create Stripe Checkout Session
        success_url = os.getenv(
            "STRIPE_SUCCESS_URL",
            "http://localhost:5173/order/success?session_id={CHECKOUT_SESSION_ID}"
        )
        cancel_url = os.getenv("STRIPE_CANCEL_URL", "http://localhost:5173/cart")

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "user_id": user_id,
                    "cart_snapshot": json.dumps(cart_snapshot),
                },
            )
        except stripe.StripeError as e:
            raise HTTPException(status_code=502, detail=f"Stripe error: {str(e)}")

        return {
            "checkout_url": session.url,
            "session_id": session.id,
        }

    # Handle the checkout.session.completed webhook event
    def handle_checkout_completed(db: Session, session: dict):
        stripe_session_id = session["id"]
        payment_intent_id = session.get("payment_intent")

        # Idempotency check: skip if already processed
        existing = db.query(Payment).filter(
            Payment.stripe_session_id == stripe_session_id
        ).first()
        if existing:
            return

        # Extract cart data from metadata
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")
        cart_snapshot_raw = metadata.get("cart_snapshot")

        if not user_id or not cart_snapshot_raw:
            return

        cart_snapshot = json.loads(cart_snapshot_raw)

        # Create the order + order items + payment
        OrderService.create_order_from_cart_data(
            db, user_id, cart_snapshot, payment_intent_id, stripe_session_id
        )

        # Decrement product stock
        for item in cart_snapshot:
            product = db.query(Product).filter(Product.id == item["product_id"]).first()
            if product:
                product.stock = max(0, product.stock - item["quantity"])

        # Clear the user's cart
        db.query(Cart).filter(Cart.user_id == user_id).delete()

        db.commit()
