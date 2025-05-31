from ninja import Schema
from datetime import datetime

class DiscussionIn(Schema):
    title: str
    content: str
    related_content_id: int

class DiscussionOut(Schema):
    id: int
    title: str
    content: str
    author_id: int
    related_content_id: int
    is_closed: bool
    created_at: datetime
    updated_at: datetime
