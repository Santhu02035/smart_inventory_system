from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.services import purchase_service

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/", response_model=PurchaseResponse)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    return purchase_service.create_purchase(db, purchase)

@router.get("/", response_model=list[PurchaseResponse])
def get_purchases(db: Session = Depends(get_db)):
    return purchase_service.get_all_purchases(db)