from ninja import Schema
from typing import List, Optional
from datetime import datetime

class ContentIn(Schema):
    title: str
    description: str
    type: str
    url: Optional[str] = None
    tags: List[str]

class ContentOut(Schema):
    id: int
    title: str
    description: str
    type: str
    url: Optional[str] = None
    tags: List[str]
    created_by_id: int
    created_at: datetime
    updated_at: datetime
