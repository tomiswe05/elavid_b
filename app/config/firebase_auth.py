import os
import json
from typing import Optional
from fastapi import Header, Depends, HTTPException
import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    if not firebase_admin._apps:
        firebase_json = os.getenv("FIREBASE_JSON")
        if not firebase_json:
            raise ValueError("FIREBASE_JSON environment variable not set")
        cred = credentials.Certificate(json.loads(firebase_json))
        firebase_admin.initialize_app(cred)


async def get_authorization_header(authorization: Optional[str] = Header(None, alias="Authorization")) -> str:
    """
    Dependency to extract and validate Authorization header
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format. Expected 'Bearer <token>'"
        )

    return authorization


async def verify_firebase_token(authorization: str = Depends(get_authorization_header)) -> str:
    """
    Dependency to verify Firebase ID token and return the user's Firebase UID

    Usage:
        @router.get("/protected")
        async def protected_route(firebase_uid: str = Depends(verify_firebase_token)):
            # firebase_uid contains the authenticated user's Firebase UID
            return {"user_id": firebase_uid}
    """
    try:
        # Extract token from "Bearer <token>"
        token = authorization.split("Bearer ")[1].strip()

        # Verify the token with Firebase
        decoded_token = auth.verify_id_token(token)

        # Return the user's Firebase UID
        return decoded_token["uid"]

    except IndexError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token verification failed: {str(e)}"
        )


async def verify_firebase_token_full(authorization: str = Depends(get_authorization_header)) -> str:

    try:
        # Extract token from "Bearer <token>"
        token = authorization.split("Bearer ")[1].strip()

        # Verify the token with Firebase
        decoded_token = auth.verify_id_token(token)

        # Return the user's Firebase UID, name and email
        return decoded_token

    except IndexError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token verification failed: {str(e)}"
        )
