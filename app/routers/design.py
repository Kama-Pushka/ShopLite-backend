from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import StoreDesign, Store, get_db
from app.schemas.design import StoreDesignUpdate, StoreDesignOut

router = APIRouter(prefix="/store-design", tags=["Store Design"])


@router.get("/{store_id}", response_model=StoreDesignOut)
async def get_design(store_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StoreDesign).where(StoreDesign.store_id == store_id))
    row = q.scalar()
    if not row:
        raise HTTPException(404, "Design not found")
    return row


@router.put("/{store_id}", response_model=StoreDesignOut)
async def update_design(store_id: int, payload: StoreDesignUpdate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StoreDesign).where(StoreDesign.store_id == store_id))
    design = q.scalar()

    if not design:
        design = StoreDesign(store_id=store_id)
        db.add(design)

    for key, value in payload.dict().items():
        setattr(design, key, value)

    await db.commit()
    await db.refresh(design)
    return design
