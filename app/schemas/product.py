from pydantic import BaseModel
from typing import Optional, Any, List


class ProductBase(BaseModel):
    store_id: int
    category_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    compare_at_price: Optional[float] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    stock: Optional[int] = 0
    status: Optional[str] = "active"
    images: Optional[Any] = None       # JSONB
    variants: Optional[Any] = None     # JSONB
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
