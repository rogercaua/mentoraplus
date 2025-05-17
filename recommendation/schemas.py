from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from user.schemas import UserOut

class RecommendationIn(BaseModel):
    title: str
    description: str
    type: str  # "roadmap" ou "course"

class RecommendationUpdate(BaseModel):
    status: str  # "pending", "approved" ou "rejected"
    reviewed_by: Optional[UserOut] = None  

class RecommendationOut(BaseModel):
    id: int
    title: str
    description: str
    type: str
    status: str
    suggested_by: UserOut        # objeto user, não só id
    reviewed_by: Optional[UserOut]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
