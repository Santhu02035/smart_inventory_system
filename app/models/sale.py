from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date
class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    selling_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_date = Column(Date, default=date.today)

    product = relationship("Product")