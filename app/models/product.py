from sqlalchemy import Column, Integer, String, Float
from app.database import Base
class Product(Base):
    __tablename__ = "products"
    id=Column(Integer, primary_key=True, index=True)
    name= Column(String, nullable=False)
    category= Column(String, nullable=False)
    brand= Column(String)
    size= Column(String)
    color= Column(String)
    purchase_price= Column(Float, nullable=False)
    selling_price= Column(Float, nullable=False)
    quantity_bought= Column(Integer, default=0)
    quantity_sold= Column(Integer, default=0)
    city= Column(String)