from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sale import Sale
from app.schemas.sale import SaleCreate


def create_sale(db: Session, sale: SaleCreate):
    db_sale = Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_all_sales(db: Session):
    return db.query(Sale).all()

def get_sales_by_product(db: Session, product_id: int):
    return db.query(Sale).filter(Sale.product_id == product_id).all()

def get_total_sold_quantity(db: Session, product_id: int):
    total = db.query(func.sum(Sale.quantity))\
              .filter(Sale.product_id == product_id)\
              .scalar()
    return total or 0