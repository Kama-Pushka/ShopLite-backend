from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Category, get_db
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/store/{store_id}", response_model=list[CategoryOut])
async def get_categories(store_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Category).where(Category.store_id == store_id))
    return rows.scalars().all()


@router.post("/", response_model=CategoryOut)
async def create_category(payload: CategoryCreate, db: AsyncSession = Depends(get_db)):
    category = Category(**payload.dict())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.put("/{cat_id}", response_model=CategoryOut)
async def update_category(cat_id: int, payload: CategoryCreate, db: AsyncSession = Depends(get_db)):
    row = await db.get(Category, cat_id)
    if not row:
        raise HTTPException(404, "Category not found")

    for k, v in payload.dict().items():
        setattr(row, k, v)

    await db.commit()
    await db.refresh(row)
    return row


@router.delete("/{cat_id}")
async def delete_category(cat_id: int, db: AsyncSession = Depends(get_db)):
    row = await db.get(Category, cat_id)
    if not row:
        raise HTTPException(404, "Category not found")
    await db.delete(row)
    await db.commit()
    return {"status": "ok"}
