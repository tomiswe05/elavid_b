from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.product import Product


class CartService:

    # Get all cart items for a user
    def get_cart(db: Session, user_id: str):
        return db.query(Cart).filter(Cart.user_id == user_id).all()

    # Add a product to cart (if already in cart, increase quantity)
    def add_to_cart(db: Session, user_id: str, product_id: int, quantity: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        existing = db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.product_id == product_id
        ).first()

        if existing:
            existing.quantity += quantity
            db.commit()
            db.refresh(existing)
            return existing

        new_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    # Update quantity of a cart item
    def update_cart_item(db: Session, user_id: str, product_id: int, quantity: int):
        item = db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.product_id == product_id
        ).first()

        if not item:
            return None

        item.quantity = quantity
        db.commit()
        db.refresh(item)
        return item

    # Remove a product from cart
    def remove_from_cart(db: Session, user_id: str, product_id: int):
        item = db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.product_id == product_id
        ).first()

        if not item:
            return False

        db.delete(item)
        db.commit()
        return True
