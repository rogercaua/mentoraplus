from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserIn(BaseModel):
    username: constr(min_length=3, max_length=150)
    email: EmailStr
    password: constr(min_length=6)
    role: Optional[str] = "user"  # padrão para usuário comum

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # Para aceitar objetos ORM do Django

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str
