from pydantic import BaseModel

class StoreCreate(BaseModel):
    name: str
    description: str | None = None
    color: str | None = None

class StoreOut(StoreCreate):
    id: int
    slug: str
    created_at: str

    class Config:
        orm_mode = True
