from pydantic import BaseModel
from datetime import date
from typing import Optional
class SaleBase(BaseModel):
    product_id: int
    selling_price: float
    quantity: int
    sale_date: Optional[date] = None

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
    class Config:
        from_attributes = True