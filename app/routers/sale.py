from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.services import sale_service
from app.auth.roles import require_staff

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/")
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_staff)
):
    return sale_service.create_sale(db, sale)

@router.get("/", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return sale_service.get_all_sales(db)