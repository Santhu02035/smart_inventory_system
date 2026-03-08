from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import product as product_model
from app.models import purchase as purchase_model
from app.models import sale as sale_model
from app.services import analytics_service
from app.auth.dependencies import get_current_user
from app.auth.roles import require_staff, require_admin
from app.models.user import User
from app.models.audit_log import AuditLog
router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/stock/{product_id}")
def get_stock(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Check if product exists
    product = db.query(product_model.Product).filter(
        product_model.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_purchased = db.query(
        func.coalesce(func.sum(purchase_model.Purchase.quantity), 0)
    ).filter(
        purchase_model.Purchase.product_id == product_id
    ).scalar()

    total_sold = db.query(
        func.coalesce(func.sum(sale_model.Sale.quantity), 0)
    ).filter(
        sale_model.Sale.product_id == product_id
    ).scalar()

    current_stock = total_purchased - total_sold

    return {
        "product_id": product_id,
        "product_name": product.name,
        "total_purchased": total_purchased,
        "total_sold": total_sold,
        "current_stock": current_stock
    }

@router.get("/profit/monthly")
def get_monthly_profit(year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.calculate_monthly_profit(db, year, month)

@router.get("/low-stock")
def low_stock(threshold: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_low_stock_products(db, threshold)

@router.get("/dead-stock")
def dead_stock(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_dead_stock_products(db)

@router.get("/top-selling")
def top_selling(
    db: Session = Depends(get_db),
    current_user = Depends(require_staff)
):
    return analytics_service.get_top_selling_products(db)

@router.get("/profit/{product_id}")
def get_profit(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.calculate_profit(db, product_id)

@router.get("/top-profitable")
def top_profitable(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_top_profitable_products(db)

@router.get("/inventory-valuation")
def inventory_valuation(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_inventory_valuation(db)

@router.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()

    return logs