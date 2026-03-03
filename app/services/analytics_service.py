from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.purchase import Purchase
from app.models.sale import Sale
from datetime import datetime
from app.models.product import Product
from app.services.purchase_service import get_total_purchased_quantity
from app.services.sale_service import get_total_sold_quantity
from sqlalchemy import desc

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

def get_top_selling_products(db: Session):

    results = (
        db.query(
            Product.id,
            Product.name,
            func.coalesce(func.sum(Sale.quantity), 0).label("total_sold")
        )
        .outerjoin(Sale, Product.id == Sale.product_id)
        .group_by(Product.id)
        .order_by(desc("total_sold"))
        .all()
    )

    return [
        {
            "product_id": r.id,
            "product_name": r.name,
            "total_sold": r.total_sold
        }
        for r in results
    ]

def get_top_profitable_products(db: Session):

    revenue_subquery = (
        db.query(
            Sale.product_id,
            func.sum(Sale.quantity * Sale.selling_price).label("revenue")
        )
        .group_by(Sale.product_id)
        .subquery()
    )

    cost_subquery = (
        db.query(
            Purchase.product_id,
            func.sum(Purchase.quantity * Purchase.purchase_price).label("cost")
        )
        .group_by(Purchase.product_id)
        .subquery()
    )

    results = (
        db.query(
            Product.id,
            Product.name,
            func.coalesce(revenue_subquery.c.revenue, 0).label("revenue"),
            func.coalesce(cost_subquery.c.cost, 0).label("cost"),
            (
                func.coalesce(revenue_subquery.c.revenue, 0)
                - func.coalesce(cost_subquery.c.cost, 0)
            ).label("profit")
        )
        .outerjoin(revenue_subquery, Product.id == revenue_subquery.c.product_id)
        .outerjoin(cost_subquery, Product.id == cost_subquery.c.product_id)
        .order_by(desc("profit"))
        .all()
    )

    return [
        {
            "product_id": r.id,
            "product_name": r.name,
            "revenue": r.revenue,
            "cost": r.cost,
            "profit": r.profit
        }
        for r in results
    ]

def get_dead_stock_products(db: Session):

    results = (
        db.query(
            Product.id,
            Product.name,
            func.coalesce(func.sum(Sale.quantity), 0).label("total_sold"),
            func.coalesce(func.sum(Purchase.quantity), 0).label("total_purchased")
        )
        .outerjoin(Sale, Product.id == Sale.product_id)
        .outerjoin(Purchase, Product.id == Purchase.product_id)
        .group_by(Product.id)
        .having(func.coalesce(func.sum(Sale.quantity), 0) == 0)
        .all()
    )

    return [
        {
            "product_id": r.id,
            "product_name": r.name,
            "total_purchased": r.total_purchased,
            "total_sold": r.total_sold
        }
        for r in results
    ]

def get_inventory_valuation(db: Session):

    products = db.query(Product).all()
    valuation_list = []
    total_inventory_value = 0

    for product in products:

        total_purchased = db.query(
            func.sum(Purchase.quantity)
        ).filter(
            Purchase.product_id == product.id
        ).scalar() or 0

        total_sold = db.query(
            func.sum(Sale.quantity)
        ).filter(
            Sale.product_id == product.id
        ).scalar() or 0

        total_cost = db.query(
            func.sum(Purchase.quantity * Purchase.purchase_price)
        ).filter(
            Purchase.product_id == product.id
        ).scalar() or 0

        current_stock = total_purchased - total_sold

        avg_purchase_price = (
            total_cost / total_purchased
            if total_purchased > 0 else 0
        )

        inventory_value = current_stock * avg_purchase_price

        total_inventory_value += inventory_value

        valuation_list.append({
            "product_id": product.id,
            "product_name": product.name,
            "current_stock": current_stock,
            "inventory_value": inventory_value
        })

    return {
        "total_inventory_value": total_inventory_value,
        "products": valuation_list
    }