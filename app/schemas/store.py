from pydantic import BaseModel
from datetime import datetime

class StoreCreate(BaseModel):
    name: str
    description: str | None = None
    color: str | None = None
    slug: str | None = None
    logo_url: str | None = None

class StoreOut(StoreCreate):
    id: int
    name: str
    slug: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


class PublishedStoreOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    color: str | None = None
    logo_url: str | None = None
    domain: str | None = None
    design_data: dict | None = None
    theme: dict | None = None
    custom_css: str | None = None
    version: int | None = None
    published: bool = True
    published_url: str
