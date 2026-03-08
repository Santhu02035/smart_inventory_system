from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.services import purchase_service
from app.auth.roles import require_admin

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/")
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return purchase_service.create_purchase(db, purchase)

@router.get("/", response_model=list[PurchaseResponse])
def get_purchases(db: Session = Depends(get_db)):
    return purchase_service.get_all_purchases(db)