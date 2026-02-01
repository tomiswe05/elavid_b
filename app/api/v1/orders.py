from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.config.firebase_auth import verify_firebase_token
from app.services.order_service import OrderService
from app.schemas.order import OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get(
    "/",
    response_model=List[OrderOut],
    summary="Get user orders",
    description="Returns all orders for the authenticated user, sorted by most recent first."
)
async def get_orders(
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    try:
        orders = OrderService.get_user_orders(db, firebase_uid)
        return orders
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch orders"
        )


@router.get(
    "/{order_id}",
    response_model=OrderOut,
    summary="Get a single order",
    description="Returns a single order by ID. Only accessible by the order owner."
)
async def get_order(
    order_id: int,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    order = OrderService.get_order_by_id(db, firebase_uid, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
