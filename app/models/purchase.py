from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date
class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    purchase_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    city = Column(String)
    wholesaler_name = Column(String)
    purchase_date = Column(Date, default=date.today)

    product = relationship("Product")