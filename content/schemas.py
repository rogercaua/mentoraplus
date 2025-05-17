from ninja import Schema
from typing import List, Optional
from datetime import datetime
from user.schemas import UserOut

class ContentBase(Schema):
    title: str
    description: str
    type: str
    tags: Optional[List[str]] = []

class ContentIn(ContentBase):
    pass

class ContentUpdate(Schema):
    title: Optional[str]
    description: Optional[str]
    type: Optional[str]
    tags: Optional[List[str]]

class ContentOut(ContentBase):
    id: int
    created_by: UserOut
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
