from pydantic import BaseModel
from typing import Optional, Any, List


class ProductBase(BaseModel):
    store_id: int | None = None
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


class ProductForm(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    status: Optional[str] = "active"
    quantity: Optional[int] = 0
    category_id: Optional[int] = None
    compare_at_price: Optional[float] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    images: Optional[List[Any]] = None
    variants: Optional[Any] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    hasLimit: Optional[bool] = None

    class Config:
        extra = "ignore"
