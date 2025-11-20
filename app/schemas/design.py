from pydantic import BaseModel
from typing import Optional, Any


class StoreDesignUpdate(BaseModel):
    design_data: Optional[Any] = None
    theme: Optional[Any] = None
    custom_css: Optional[str] = None
    is_published: Optional[bool] = None
    version: Optional[int] = None


class StoreDesignOut(StoreDesignUpdate):
    id: int
    store_id: int

    class Config:
        orm_mode = True
