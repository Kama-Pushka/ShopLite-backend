from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Collection, CollectionProduct, get_db
from app.schemas.collection import CollectionCreate, CollectionOut

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get("/store/{store_id}", response_model=list[CollectionOut])
async def get_collections(store_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Collection).where(Collection.store_id == store_id))
    return rows.scalars().all()


@router.post("/", response_model=CollectionOut)
async def create_collection(payload: CollectionCreate, db: AsyncSession = Depends(get_db)):
    coll = Collection(**payload.dict())
    db.add(coll)
    await db.commit()
    await db.refresh(coll)
    return coll


@router.post("/{collection_id}/products/{product_id}")
async def add_product(collection_id: int, product_id: int, db: AsyncSession = Depends(get_db)):
    link = CollectionProduct(collection_id=collection_id, product_id=product_id)
    db.add(link)
    await db.commit()
    return {"status": "added"}
