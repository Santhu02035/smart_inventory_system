from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.services import sale_service
from app.auth.roles import require_staff,require_admin
from app.services.audit_service import create_audit_log

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=SaleResponse)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_staff)
):

    new_sale = sale_service.create_sale(db, sale)

    create_audit_log(
        db,
        username=current_user.username,
        action="CREATE_SALE",
        entity="Sale",
        details=f"Sold {sale.quantity} units of product {sale.product_id}"
    )

    return new_sale

@router.get("/", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return sale_service.get_all_sales(db)