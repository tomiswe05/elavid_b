from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    # Get all products from database
    def get_all_products(db: Session):
        return db.query(Product).all()

    # Get a single product by its id
    def get_product_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    # Create a new product
    def create_product(db: Session, product_data: ProductCreate):
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
            image_url=product_data.image_url,
            category=product_data.category
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    # Update an existing product (only updates fields that are provided)
    def update_product(db: Session, product_id: int, product_data: ProductUpdate):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product

    # Delete a product
    def delete_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False

        db.delete(product)
        db.commit()
        return True
