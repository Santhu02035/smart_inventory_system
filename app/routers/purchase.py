from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.services import purchase_service
from app.auth.roles import require_admin, require_staff
from app.services.audit_service import create_audit_log

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/", response_model=PurchaseResponse)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_staff)
):

    new_purchase = purchase_service.create_purchase(db, purchase)

    create_audit_log(
        db,
        username=current_user.username,
        action="ADD_PURCHASE",
        entity="Purchase",
        details=f"Purchased {purchase.quantity} units of product {purchase.product_id}"
    )

    return new_purchase

@router.get("/", response_model=list[PurchaseResponse])
def get_purchases(db: Session = Depends(get_db)):
    return purchase_service.get_all_purchases(db)