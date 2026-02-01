from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Schema for returning user data from the API
class UserOut(BaseModel):
    id: str  # Firebase UID
    name: Optional[str]
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
