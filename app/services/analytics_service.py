from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.purchase import Purchase
from app.models.sale import Sale
from datetime import datetime
from app.models.product import Product
from app.services.purchase_service import get_total_purchased_quantity
from app.services.sale_service import get_total_sold_quantity

def calculate_profit(db: Session, product_id: int):

    total_revenue = db.query(
        func.sum(Sale.quantity * Sale.selling_price)
    ).filter(
        Sale.product_id == product_id
    ).scalar() or 0

    total_cost = db.query(
        func.sum(Purchase.quantity * Purchase.purchase_price)
    ).filter(
        Purchase.product_id == product_id
    ).scalar() or 0

    profit = total_revenue - total_cost
    return {
        "product_id": product_id,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "profit": profit
    }

def calculate_monthly_profit(db: Session, year: int, month: int):

    start_date = datetime(year, month, 1)

    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    total_revenue = db.query(
        func.sum(Sale.quantity * Sale.selling_price)
    ).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date < end_date
    ).scalar() or 0

    total_cost = db.query(
        func.sum(Purchase.quantity * Purchase.purchase_price)
    ).filter(
        Purchase.purchase_date >= start_date,
        Purchase.purchase_date < end_date
    ).scalar() or 0

    profit = total_revenue - total_cost

    return {
        "year": year,
        "month": month,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "profit": profit
    }

def get_low_stock_products(db: Session, threshold: int):

    products = db.query(Product).all()
    low_stock_list = []

    for product in products:
        total_purchased = get_total_purchased_quantity(db, product.id)
        total_sold = get_total_sold_quantity(db, product.id)

        current_stock = total_purchased - total_sold

        if current_stock <= threshold:
            low_stock_list.append({
                "product_id": product.id,
                "product_name": product.name,
                "current_stock": current_stock
            })

    return {
        "threshold": threshold,
        "low_stock_products": low_stock_list
    }