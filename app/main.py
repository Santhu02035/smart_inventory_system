from fastapi import FastAPI
from app.database import engine, Base
from app.models import product, purchase, sale
from app.routers import product, purchase, sale
from app.routers import analytics

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(product.router)
app.include_router(purchase.router)
app.include_router(sale.router)
app.include_router(analytics.router)

@app.get("/")
def home():
    return {"message": "Smart Inventory System API Running"}
