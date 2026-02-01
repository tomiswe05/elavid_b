from dotenv import load_dotenv
load_dotenv()  # Reads the .env file and loads variables into os.getenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.firebase_auth import initialize_firebase
from app.config.database import engine, Base
import app.models  # noqa: F401
from app.api.v1 import users, products, cart, orders, payments

app = FastAPI(title="Elavid API")

initialize_firebase()
Base.metadata.create_all(bind=engine)

# Register all route files under /api/v1
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")

# CORS (Cross-Origin Resource Sharing) middleware
# Your React frontend runs on localhost:5173, your backend on localhost:8000
# Browsers block requests between different origins by default for security
# This middleware tells the browser: "it's okay, allow requests from my frontend"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your Vite dev server
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],     # Allow all headers (including Authorization)
)


@app.get("/")
def root():
    """Health check endpoint - just confirms the API is running"""
    return {"message": "Elavid API is running"}
