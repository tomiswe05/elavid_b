import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.config.firebase_auth import verify_firebase_token
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])

ADMIN_UIDS = [uid.strip() for uid in os.getenv("ADMIN_UIDS", "").split(",") if uid.strip()]


@router.get(
    "/",
    response_model=List[ProductOut],
    summary="Get all products",
    description="Returns a list of all available products. No authentication required."
)
async def get_all_products(db: Session = Depends(get_db)):
    try:
        products = ProductService.get_all_products(db)
        return products
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch products"
        )


@router.get(
    "/{product_id}",
    response_model=ProductOut,
    summary="Get a product by ID",
    description="Returns a single product by its ID. Returns 404 if the product does not exist."
)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post(
    "/",
    response_model=ProductOut,
    summary="Create a product",
    description="Creates a new product. Admin only."
)
async def create_product(
    product_data: ProductCreate,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    if firebase_uid not in ADMIN_UIDS:
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        product = ProductService.create_product(db, product_data)
        return product
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create product"
        )


@router.put(
    "/{product_id}",
    response_model=ProductOut,
    summary="Update a product",
    description="Updates an existing product. Only provided fields will be changed. Admin only."
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    if firebase_uid not in ADMIN_UIDS:
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        product = ProductService.update_product(db, product_id, product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update product"
        )


@router.delete(
    "/{product_id}",
    summary="Delete a product",
    description="Deletes a product by its ID. Admin only."
)
async def delete_product(
    product_id: int,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    if firebase_uid not in ADMIN_UIDS:
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        deleted = ProductService.delete_product(db, product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete product"
        )
