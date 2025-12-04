from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Product, get_db
from app.schemas.product import ProductCreate, ProductForm, ProductOut

router = APIRouter(tags=["Products"])


async def _get_product(db: AsyncSession, prod_id: int, store_id: int | None = None) -> Product:
    product = await db.get(Product, prod_id)
    if not product:
        raise HTTPException(404, "Product not found")
    if store_id is not None and product.store_id != store_id:
        raise HTTPException(404, "Product not found for this store")
    return product


def _prepare_product_data(store_id: int, payload: dict) -> dict:
    data = payload.copy()
    data["store_id"] = store_id

    if "quantity" in data:
        data["stock"] = data.pop("quantity") or 0

    variants = data.pop("variants", {}) or {}
    if data.get("size"):
        variants["size"] = data.pop("size")
    if data.get("color"):
        variants["color"] = data.pop("color")
    if "hasLimit" in data:
        variants["hasLimit"] = data.pop("hasLimit")
    if variants:
        data["variants"] = variants

    data.pop("id", None)
    return data


@router.get("/products/store/{store_id}", response_model=list[ProductOut])
@router.get("/stores/{store_id}/products", response_model=list[ProductOut])
async def get_products(store_id: int, status: str = "all", db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.store_id == store_id)
    if status != "all":
        query = query.where(Product.status == status)
    rows = await db.execute(query)
    return rows.scalars().all()


@router.get("/products/{prod_id}", response_model=ProductOut)
async def get_product(prod_id: int, db: AsyncSession = Depends(get_db)):
    return await _get_product(db, prod_id)


@router.post("/products", response_model=ProductOut)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    if not payload.store_id:
        raise HTTPException(400, "store_id is required")

    prod = Product(**_prepare_product_data(payload.store_id, payload.dict()))
    db.add(prod)
    await db.commit()
    await db.refresh(prod)
    return prod


@router.post("/stores/{store_id}/products", response_model=ProductOut)
async def create_store_product(store_id: int, payload: ProductForm, db: AsyncSession = Depends(get_db)):
    prod = Product(**_prepare_product_data(store_id, payload.dict()))
    db.add(prod)
    await db.commit()
    await db.refresh(prod)
    return prod


@router.put("/products/{prod_id}", response_model=ProductOut)
async def update_product(prod_id: int, payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    row = await _get_product(db, prod_id)

    data = _prepare_product_data(payload.store_id or row.store_id, payload.dict(exclude_unset=True))
    for k, v in data.items():
        setattr(row, k, v)

    await db.commit()
    await db.refresh(row)
    return row


@router.put("/stores/{store_id}/products/{prod_id}", response_model=ProductOut)
async def update_store_product(store_id: int, prod_id: int, payload: ProductForm, db: AsyncSession = Depends(get_db)):
    row = await _get_product(db, prod_id, store_id)
    data = _prepare_product_data(store_id, payload.dict(exclude_unset=True))
    for k, v in data.items():
        setattr(row, k, v)

    await db.commit()
    await db.refresh(row)
    return row


@router.delete("/products/{prod_id}")
async def delete_product(prod_id: int, db: AsyncSession = Depends(get_db)):
    row = await _get_product(db, prod_id)
    await db.delete(row)
    await db.commit()
    return {"status": "ok"}


@router.delete("/stores/{store_id}/products/{prod_id}")
async def delete_store_product(store_id: int, prod_id: int, db: AsyncSession = Depends(get_db)):
    row = await _get_product(db, prod_id, store_id)
    await db.delete(row)
    await db.commit()
    return {"status": "ok"}
