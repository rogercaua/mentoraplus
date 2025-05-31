from ninja import Schema
from pydantic import EmailStr
from typing import Optional

class UserIn(Schema):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"  # padrão para usuário comum

class UserOut(Schema):
    id: int
    username: str
    email: EmailStr
    role: str

class SelfOut(Schema):
    id: int
    username: str
    email: EmailStr

class LoginIn(Schema):
    email: EmailStr
    password: str

class LoginOut(Schema):
    access_token: str
    token_type: str
