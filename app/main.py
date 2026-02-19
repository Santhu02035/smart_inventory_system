from fastapi import FastAPI
from app.database import engine
from app.models import product
from app.database import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Smart Inventory System API Running"}
