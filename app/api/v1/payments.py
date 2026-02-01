import os
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.firebase_auth import verify_firebase_token
from app.services.payment_service import PaymentService
from app.schemas.order import CheckoutSessionOut

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/checkout",
    response_model=CheckoutSessionOut,
    summary="Create Stripe Checkout session",
    description="Creates a Stripe Checkout session from the user's cart. Returns the checkout URL for client redirect."
)
async def create_checkout_session(
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    try:
        result = PaymentService.create_checkout_session(db, firebase_uid)
        return result
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create checkout session"
        )


@router.post(
    "/webhook/stripe",
    summary="Stripe webhook",
    description="Receives Stripe webhook events. Verifies the signature and processes checkout.session.completed events."
)
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        try:
            PaymentService.handle_checkout_completed(db, session)
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to process webhook"
            )

    return {"status": "ok"}
