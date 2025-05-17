from ninja import Router
from typing import List
from .models import Comment
from .schemas import CommentIn, CommentOut, CommentUpdate
from user.auth import auth
from django.shortcuts import get_object_or_404
from datetime import datetime

router = Router()

@router.post("/", response=CommentOut, auth=auth)
def create_comment(request, data: CommentIn):
    """
    Cria um novo comentário em uma discussão.

    - **text**: texto do comentário.
    - **discussion_id**: id da discussão relacionada.
    - **author**: usuário autenticado que criou o comentário.

    Retorna o comentário criado.
    """
    comment = Comment.objects.create(
        text=data.text,
        discussion_id=data.discussion_id,
        author=request.user
    )
    return comment

@router.get("/", response=List[CommentOut])
def list_comments(request):
    """
    Lista todos os comentários existentes.
    """
    return Comment.objects.all()

@router.get("/{comment_id}", response=CommentOut)
def get_comment(request, comment_id: int):
    """
    Retorna um comentário específico pelo seu ID.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    return comment

@router.put("/{comment_id}", response=CommentOut, auth=auth)
def update_comment(request, comment_id: int, data: CommentUpdate):
    """
    Atualiza um comentário existente.

    Apenas o autor do comentário ou um admin pode atualizar.

    - Atualiza os campos enviados no payload.

    Retorna o comentário atualizado.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user and request.user.role != "admin":
        return {"error": "Not authorized"}
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(comment, attr, value)
    comment.save()
    return comment

@router.delete("/{comment_id}", auth=auth)
def delete_comment(request, comment_id: int):
    """
    Deleta um comentário.

    Apenas o autor do comentário ou um admin pode deletar.

    Retorna um JSON indicando sucesso.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user and request.user.role != "admin":
        return {"error": "Not authorized"}
    comment.delete()
    return {"success": True}

@router.get("/search/", response=List[CommentOut])
def search_comments(request, q: str = None):
    """
    Busca comentários pelo texto.

    - Parâmetro `q`: termo para busca dentro do texto do comentário.
    - Retorna todos os comentários se `q` não informado ou vazio.
    """
    if not q:
        return Comment.objects.all()
    return Comment.objects.filter(text__icontains=q)
