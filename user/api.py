from ninja import Router
from .models import User
from mentoraplus.responses import MessageOut
from .schemas import UserIn, UserOut,SelfOut, LoginIn, LoginOut
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from typing import List
from datetime import datetime, timedelta
from jose import jwt
from ninja.errors import HttpError
from django.conf import settings
from user.auth import auth
from datetime import datetime, timedelta, timezone

router = Router(tags=["User"])

def create_jwt(user_id: int) -> str:
    """
    Cria um token JWT para o usuário autenticado.
    """
    now = datetime.now(timezone.utc)
    payload = {
        'sub': str(user_id),                   
        'iat': int(now.timestamp()),          
        'exp': int((now + timedelta(hours=1)).timestamp()),  
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

#----------------------------------------------------------------------------------------->

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
    
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, 'Nome de Usuario já existe.')
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400,'Email já existente.')
    
    user = User(
        username = data.username,
        email = data.email,
        password = make_password(data.password),
        role = data.role if data.role else 'user'
    )
    user.save()
    
    return user

#----------------------------------------------------------------------------------------->

@router.post('/login', response=LoginOut)
def login(request, data: LoginIn):
    """
    Login de usuário.
    
    -**email**: e-mail do usuário
    -**password**: senha
    
    Retorna authToken
    """
    try:
        user = User.objects.get(email=data.email) 
    except User.DoesNotExist:
        raise HttpError(401, 'Email ou senha inválidos.')
    
    if not check_password(data.password, user.password):
        raise HttpError(401, 'Email ou senha inválidos.')
    
    token = create_jwt(user.id)
    
    return {'access_token': token, 'token_type': 'bearer'}

#----------------------------------------------------------------------------------------->

@router.get("/me", response=SelfOut, auth=auth)
def me(request):
    """
    Retorna os dados do usuário autenticado.

    Requer token JWT válido.
    """
    user = request.user
    if not user:
        raise HttpError(401, "Usuário não autenticado")
    
    return user

#----------------------------------------------------------------------------------------->

@router.get("/all", response=List[UserOut], auth=auth)
def list_users(request):
    """
    Lista todos os usuários do sistema.

    Requer que o usuário autenticado seja admin.
    """
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    
    users = User.objects.all()

    return users

#----------------------------------------------------------------------------------------->

@router.delete("/delete/{user_id}", response=MessageOut, auth=auth)
def delete_user(request,user_id: int):
    """
    Deleta um usuário, utilizando-se o ID.

    - **user_id**: ID do usuário a ser deletado
    - **auth**: token JWT do usuário autenticado
    
    -Usuário com role 'user' pode deletar sua própria conta.
    -Usuário com role 'admin' pode deletar qualquer conta.
    
    Requer autenticação do usuário.
    """
    user = get_object_or_404(User, id=user_id)
    
    if request.user.role == "user" and request.user.id != user.id:
        raise HttpError(403, "Não autorizado")
        
    User.delete(user)
    return {"message": f"Usuário **{user.username}** deletado com sucesso."}
    
