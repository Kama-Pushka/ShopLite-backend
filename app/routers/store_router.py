from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Store, get_db, User
from app.schemas.store import StoreCreate, StoreOut
from app.services.auth_service import AuthService
router = APIRouter(prefix="/stores", tags=["Stores"])


@router.get("/", response_model=list[StoreOut])
async def get_stores(
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = await db.execute(
        select(Store).where(Store.user_id == current_user.id)
    )
    
    return rows.scalars().all()

@router.get("/{store_id}", response_model=StoreOut)
async def get_store(store_id: int, db: AsyncSession = Depends(get_db)):
    row = await db.get(Store, store_id)
    if not row:
        raise HTTPException(404, "Store not found")
    return row


@router.post("/", response_model=StoreOut)
async def create_store(payload: StoreCreate,
                       current_user: User = Depends(AuthService.get_current_user),
                       db: AsyncSession = Depends(get_db)):
    store = Store(
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        color=payload.color,
        slug=payload.slug,
        logo_url=payload.logo_url,
    )
    
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store


@router.put("/{store_id}", response_model=StoreOut)
async def update_store(store_id: int, payload: StoreCreate, db: AsyncSession = Depends(get_db)):
    store = await db.get(Store, store_id)
    if not store:
        raise HTTPException(404, "Store not found")

    for key, value in payload.dict().items():
        setattr(store, key, value)

    await db.commit()
    await db.refresh(store)
    return store


@router.delete("/{store_id}")
async def delete_store(store_id: int, db: AsyncSession = Depends(get_db)):
    row = await db.get(Store, store_id)
    if not row:
        raise HTTPException(404, "Store not found")

    await db.delete(row)
    await db.commit()
    return {"status": "ok"}
