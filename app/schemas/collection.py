from pydantic import BaseModel
from typing import Optional


class CollectionBase(BaseModel):
    store_id: int
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True
    order_index: Optional[int] = 0


class CollectionCreate(CollectionBase):
    pass


class CollectionOut(CollectionBase):
    id: int

    class Config:
        orm_mode = True
