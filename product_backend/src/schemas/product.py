from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    image: Optional[str] = None
    description: str
    stock: float
    list_price: float
    standard_price: float
    discount: float

class ProductCreate(ProductBase):
    pass  # Igual que ProductBase, se usa para crear

class ProductUpdate(BaseModel):
    name: str
    description: str
    stock: float
    list_price: float
    standard_price: float
    discount: float
    image: Optional[str] = None

class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True
