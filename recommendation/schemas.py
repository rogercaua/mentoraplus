from ninja import Schema
from typing import Optional, List
from datetime import datetime

class RecommendationIn(Schema):
    title: str
    description: str
    type: str  # "roadmap" ou "course"
    url: Optional[str] = None
    tags: List[str]
    
class RecommendationOut(Schema):
    id: int
    title: str
    description: str
    type: str
    url: Optional[str] = None
    status: str
    suggested_by_id: int
    reviewed_by_id: Optional[int]
    created_at: datetime
    updated_at: datetime
