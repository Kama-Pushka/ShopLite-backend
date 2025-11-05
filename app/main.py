from fastapi import FastAPI
from app.routers.auth_router import router as auth_router

app = FastAPI(title="Auth Service")
app.include_router(auth_router, prefix="/v1/api")
