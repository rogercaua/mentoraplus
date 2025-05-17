from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DiscussionIn(BaseModel):
    title: str
    content: str
    related_content_id: int

class DiscussionOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    related_content_id: int
    created_at: datetime
    updated_at: datetime
    is_closed: bool
    
    class Config:
        from_attributes = True
