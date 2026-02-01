from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.firebase_auth import verify_firebase_token_full
from app.services.user_service import UserService
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/me",
    response_model=UserOut,
    summary="Get or create current user",
    description="Verifies the Firebase token, extracts user info (uid, email, name), and returns the user from the database. Creates a new user if they don't exist yet."
)
async def get_or_create_user(
    decoded_token: dict = Depends(verify_firebase_token_full),
    db: Session = Depends(get_db)
):
    uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    name = decoded_token.get("name", "")

    if not uid or not email:
        raise HTTPException(
            status_code=400,
            detail="Firebase token missing uid or email"
        )

    try:
        user = UserService.get_userdata(db, uid, name, email)
        return user
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create or retrieve user"
        )
