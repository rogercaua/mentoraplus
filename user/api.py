from ninja import Router
from .models import User
from .schemas import UserIn, UserOut, UserLogin, TokenOut
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from typing import List
from datetime import datetime, timedelta
from jose import jwt
from ninja.errors import HttpError
from django.conf import settings
from user.auth import auth  # Importa o auth modularizado

router = Router()

@router.post("/register", response=UserOut)
def register(request, data: UserIn):
    """
    Cria um novo usuário.

    - **username**: nome de usuário único
    - **email**: e-mail válido
    - **password**: senha que será armazenada com hash
    - **role**: tipo do usuário ("user" ou "admin")

    Retorna os dados do usuário criado, sem a senha.
    """
    data.password = make_password(data.password)
    user = User.objects.create(**data.model_dump())
    return UserOut.model_validate(user)

@router.post("/login", response=TokenOut)
def login(request, data: UserLogin):
    """
    Realiza login e retorna token JWT.

    - **email**: e-mail cadastrado
    - **password**: senha do usuário

    Retorna um token de acesso e o tipo do token (Bearer).
    """
    user = get_object_or_404(User, email=data.email)
    if not check_password(data.password, user.password):
        raise HttpError(401, "Credenciais inválidas")
    token_payload = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + timedelta(minutes=60),
    }
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "Bearer"}

@router.get("/me", response=UserOut, auth=auth)
def me(request):
    """
    Retorna os dados do usuário autenticado.

    Requer token JWT válido.
    """
    return UserOut.model_validate(request.user)

@router.get("/all", response=List[UserOut], auth=auth)
def list_users(request):
    """
    Lista todos os usuários do sistema.

    Requer que o usuário autenticado seja admin.
    """
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    
    users = User.objects.all()
    # Converte a queryset para lista de schemas usando list comprehension
    return [UserOut.model_validate(user) for user in users]
