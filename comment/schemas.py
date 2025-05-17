from ninja import Schema
from datetime import datetime
from typing import Optional

class CommentIn(Schema):
    text: str
    discussion_id: int  # para associar ao tópico

class CommentOut(Schema):
    id: int
    text: str
    author: int  # id do usuário
    discussion: int  # id do tópico
    created_at: datetime
    
    class Config:
        from_attributes = True

class CommentUpdate(Schema):
    text: Optional[str]

