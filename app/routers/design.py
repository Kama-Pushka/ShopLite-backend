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
        # auto-create пустой дизайн, чтобы фронт мог редактировать без 404
        row = StoreDesign(store_id=store_id, design_data={})
        db.add(row)
        await db.commit()
        await db.refresh(row)
    return row


@router.put("/{store_id}", response_model=StoreDesignOut)
async def update_design(store_id: int, payload: StoreDesignUpdate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StoreDesign).where(StoreDesign.store_id == store_id))
    design = q.scalar()

    if not design:
        design = StoreDesign(store_id=store_id, design_data={})
        db.add(design)

    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(design, key, value)

    # синхронизируем логотип магазина, если пришёл из конструктора
    store_logo = None
    if "design_data" in data:
        dd = data.get("design_data") or {}
        store_logo = dd.get("storeLogo") or dd.get("store_logo")
    if store_logo:
        store_row = await db.get(Store, store_id)
        if store_row:
            store_row.logo_url = store_logo

    await db.commit()
    await db.refresh(design)
    return design


@router.post("/{store_id}/publish", response_model=StoreDesignOut)
async def publish_design(store_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StoreDesign).where(StoreDesign.store_id == store_id))
    design = q.scalar()

    if not design:
        design = StoreDesign(store_id=store_id, design_data={}, is_published=True, version=1)
        db.add(design)
    else:
        design.is_published = True
        design.version = (design.version or 0) + 1

    await db.commit()
    await db.refresh(design)
    return design
