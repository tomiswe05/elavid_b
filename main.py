import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.firebase_auth import initialize_firebase
from app.config.database import engine, Base
import app.models  # noqa: F401
from app.api.v1 import users, products, cart, orders, payments

app = FastAPI(title="Elavid API")

initialize_firebase()
Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
origins = [o.strip() for o in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check endpoint - just confirms the API is running"""
    return {"message": "Elavid API is running"}
