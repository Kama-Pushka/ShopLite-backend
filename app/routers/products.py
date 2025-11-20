from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Product, get_db
from app.schemas.product import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/store/{store_id}", response_model=list[ProductOut])
async def get_products(store_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Product).where(Product.store_id == store_id))
    return rows.scalars().all()


@router.get("/{prod_id}", response_model=ProductOut)
async def get_product(prod_id: int, db: AsyncSession = Depends(get_db)):
    row = await db.get(Product, prod_id)
    if not row:
        raise HTTPException(404, "Product not found")
    return row


@router.post("/", response_model=ProductOut)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    prod = Product(**payload.dict())
    db.add(prod)
    await db.commit()
    await db.refresh(prod)
    return prod


@router.put("/{prod_id}", response_model=ProductOut)
async def update_product(prod_id: int, payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    row = await db.get(Product, prod_id)
    if not row:
        raise HTTPException(404, "Product not found")

    for k, v in payload.dict().items():
        setattr(row, k, v)

    await db.commit()
    await db.refresh(row)
    return row


@router.delete("/{prod_id}")
async def delete_product(prod_id: int, db: AsyncSession = Depends(get_db)):
    row = await db.get(Product, prod_id)
    if not row:
        raise HTTPException(404, "Product not found")
    await db.delete(row)
    await db.commit()
    return {"status": "ok"}
