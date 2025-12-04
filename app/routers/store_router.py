from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Store, get_db, User
from app.schemas.store import StoreCreate, StoreOut
from app.services.auth_service import AuthService
import re
import uuid
router = APIRouter(prefix="/stores", tags=["Stores"])


async def _is_slug_taken(db: AsyncSession, slug: str, exclude_store_id: int | None = None) -> bool:
    query = select(Store).where(Store.slug == slug)
    if exclude_store_id:
        query = query.where(Store.id != exclude_store_id)
    existing = await db.execute(query)
    return existing.scalars().first() is not None


async def _prepare_slug(db: AsyncSession, name: str, provided_slug: str | None, exclude_store_id: int | None = None) -> str:
    base = (provided_slug or name or "").strip().lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-") or f"store-{uuid.uuid4().hex[:6]}"
    candidate = base
    counter = 1
    while await _is_slug_taken(db, candidate, exclude_store_id=exclude_store_id):
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate


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
    slug = await _prepare_slug(db, payload.name, payload.slug)
    store = Store(
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        color=payload.color,
        slug=slug,
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

    data = payload.dict()
    if data.get("slug"):
        store.slug = await _prepare_slug(db, data.get("name") or store.name, data["slug"], exclude_store_id=store.id)
    for key, value in data.items():
        if key == "slug":
            continue
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
