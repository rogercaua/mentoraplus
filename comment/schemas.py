from ninja import Schema
from datetime import datetime

class CommentIn(Schema):
    text: str


class CommentOut(Schema):
    id: int
    text: str
    author_id: int
    discussion_id: int
    created_at: datetime