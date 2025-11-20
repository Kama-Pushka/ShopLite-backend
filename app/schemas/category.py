from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    store_id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    image_url: Optional[str] = None
    order_index: Optional[int] = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
