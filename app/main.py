from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

from app.routers.store_router import router as stores_router
from app.routers.design import router as design_router
from app.routers.products import router as products_router
from app.routers.categories import router as categories_router
from app.routers.collections import router as collections_router
from app.routers.orders import router as orders_router

app = FastAPI(title="Shoplite")

origins = [
    "http://localhost:3000",  
    "http://195.133.66.226",   
    "*",                      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/v1/api")


app.include_router(stores_router, prefix="/v1/api")
app.include_router(design_router, prefix="/v1/api")
app.include_router(products_router, prefix="/v1/api")
app.include_router(categories_router, prefix="/v1/api")
app.include_router(collections_router, prefix="/v1/api")
app.include_router(orders_router, prefix="/v1/api")


@app.get("/")
async def root():
    return {"status": "ok", "message": "Shoplite API is up"}
