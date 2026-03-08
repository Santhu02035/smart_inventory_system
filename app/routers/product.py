from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services import product_service
from app.auth.roles import require_admin
from app.services.audit_service import create_audit_log

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    new_product = product_service.create_product(db, product)

    create_audit_log(
        db,
        username=current_user.username,
        action="CREATE_PRODUCT",
        entity="Product",
        details=f"Created product {product.name}"
    )

    return new_product

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}