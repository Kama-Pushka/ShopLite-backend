from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Collection, CollectionProduct, get_db
from app.schemas.collection import CollectionCreate, CollectionOut

router = APIRouter(tags=["Collections"])


async def _get_collection(db: AsyncSession, collection_id: int, store_id: int | None = None) -> Collection:
    collection = await db.get(Collection, collection_id)
    if not collection:
        raise HTTPException(404, "Collection not found")
    if store_id is not None and collection.store_id != store_id:
        raise HTTPException(404, "Collection not found for this store")
    return collection


@router.get("/collections/store/{store_id}", response_model=list[CollectionOut])
@router.get("/stores/{store_id}/collections", response_model=list[CollectionOut])
async def get_collections(store_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Collection).where(Collection.store_id == store_id))
    return rows.scalars().all()


@router.post("/collections", response_model=CollectionOut)
async def create_collection(payload: CollectionCreate, db: AsyncSession = Depends(get_db)):
    if not payload.store_id:
        raise HTTPException(400, "store_id is required")
    coll = Collection(**payload.dict())
    db.add(coll)
    await db.commit()
    await db.refresh(coll)
    return coll


@router.post("/stores/{store_id}/collections", response_model=CollectionOut)
async def create_store_collection(store_id: int, payload: CollectionCreate, db: AsyncSession = Depends(get_db)):
    data = payload.dict()
    data["store_id"] = store_id
    coll = Collection(**data)
    db.add(coll)
    await db.commit()
    await db.refresh(coll)
    return coll


@router.put("/collections/{collection_id}", response_model=CollectionOut)
async def update_collection(collection_id: int, payload: CollectionCreate, db: AsyncSession = Depends(get_db)):
    collection = await _get_collection(db, collection_id)
    for key, value in payload.dict(exclude_unset=True).items():
        if key == "store_id":
            continue
        setattr(collection, key, value)
    await db.commit()
    await db.refresh(collection)
    return collection


@router.put("/stores/{store_id}/collections/{collection_id}", response_model=CollectionOut)
async def update_store_collection(store_id: int, collection_id: int, payload: CollectionCreate, db: AsyncSession = Depends(get_db)):
    collection = await _get_collection(db, collection_id, store_id)
    for key, value in payload.dict(exclude_unset=True).items():
        if key == "store_id":
            continue
        setattr(collection, key, value)
    await db.commit()
    await db.refresh(collection)
    return collection


@router.delete("/collections/{collection_id}")
async def delete_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    collection = await _get_collection(db, collection_id)
    await db.delete(collection)
    await db.commit()
    return {"status": "ok"}


@router.delete("/stores/{store_id}/collections/{collection_id}")
async def delete_store_collection(store_id: int, collection_id: int, db: AsyncSession = Depends(get_db)):
    collection = await _get_collection(db, collection_id, store_id)
    await db.delete(collection)
    await db.commit()
    return {"status": "ok"}


@router.post("/collections/{collection_id}/products/{product_id}")
async def add_product(collection_id: int, product_id: int, db: AsyncSession = Depends(get_db)):
    link = CollectionProduct(collection_id=collection_id, product_id=product_id)
    db.add(link)
    await db.commit()
    return {"status": "added"}
