from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseCreate

def create_purchase(db: Session, purchase: PurchaseCreate):
    db_purchase = Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def get_all_purchases(db: Session):
    return db.query(Purchase).all()

def get_purchases_by_product(db: Session, product_id: int):
    return db.query(Purchase).filter(Purchase.product_id == product_id).all()

def get_total_purchased_quantity(db: Session, product_id: int):
    total = db.query(func.sum(Purchase.quantity))\
              .filter(Purchase.product_id == product_id)\
              .scalar()
    return total or 0