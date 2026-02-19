from fastapi import FastAPI
from app.database import engine, Base
from app.models import product
from app.routers import product as product_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(product_router.router)

@app.get("/")
def home():
    return {"message": "Smart Inventory System API Running"}
