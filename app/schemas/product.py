from pydantic import BaseModel
from typing import Optional
class ProductBase(BaseModel):
    name: str
    category: str
    brand: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    purchase_price: float
    selling_price: float
    quantity_bought: int
    quantity_sold: int
    city: Optional[str] = None

class ProductCreate(ProductBase):
    pass
class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True
