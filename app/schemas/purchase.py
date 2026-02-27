from pydantic import BaseModel
from datetime import date
from typing import Optional
class PurchaseBase(BaseModel):
    product_id: int
    purchase_price: float
    quantity: int
    city: Optional[str] = None
    wholesaler_name: Optional[str] = None
    purchase_date: Optional[date] = None

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseResponse(PurchaseBase):
    id: int
    class Config:
        from_attributes = True