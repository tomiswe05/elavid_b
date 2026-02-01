from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.config.firebase_auth import verify_firebase_token
from app.services.cart_service import CartService
from app.schemas.cart import CartAdd, CartUpdate, CartItemOut

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get(
    "/",
    response_model=List[CartItemOut],
    summary="Get cart items",
    description="Returns all items in the authenticated user's cart with product details."
)
async def get_cart(
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    try:
        items = CartService.get_cart(db, firebase_uid)

        return [
            CartItemOut(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                product_name=item.product.name,
                product_price=item.product.price,
                product_image=item.product.image_url
            )
            for item in items
        ]
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch cart"
        )


@router.post(
    "/add",
    response_model=CartItemOut,
    summary="Add to cart",
    description="Adds a product to the user's cart. If the product is already in the cart, the quantity is increased."
)
async def add_to_cart(
    cart_data: CartAdd,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    try:
        item = CartService.add_to_cart(db, firebase_uid, cart_data.product_id, cart_data.quantity)

        if not item:
            raise HTTPException(status_code=404, detail="Product not found")

        return CartItemOut(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product.name,
            product_price=item.product.price,
            product_image=item.product.image_url
        )
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to add to cart"
        )


@router.put(
    "/update",
    response_model=CartItemOut,
    summary="Update cart item",
    description="Updates the quantity of a product in the user's cart."
)
async def update_cart_item(
    cart_data: CartUpdate,
    product_id: int,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    try:
        item = CartService.update_cart_item(db, firebase_uid, product_id, cart_data.quantity)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        return CartItemOut(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product.name,
            product_price=item.product.price,
            product_image=item.product.image_url
        )
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update cart item"
        )


@router.delete(
    "/remove",
    summary="Remove from cart",
    description="Removes a product from the user's cart."
)
async def remove_from_cart(
    product_id: int,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    try:
        removed = CartService.remove_from_cart(db, firebase_uid, product_id)

        if not removed:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        return {"message": "Item removed from cart"}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to remove from cart"
        )
