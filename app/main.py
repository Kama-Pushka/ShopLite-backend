from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth Service")

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
