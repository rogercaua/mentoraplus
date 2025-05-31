from ninja import Router
from typing import List
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from mentoraplus.responses import MessageOut
from .schemas import CommentOut, CommentIn
from .models import Discussion, Comment
from content.models import Content
from user.auth import auth

router = Router(tags=["Comment"])

# Criar comentário em uma discussão
@router.post("/discussions/{discussion_id}/comments", response=CommentOut, auth=auth)
def create_comment(request, discussion_id: int, data: CommentIn):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if discussion.is_closed:
        raise HttpError(400, "Discussão está fechada para novos comentários")
    comment = Comment.objects.create(
        text=data.text,
        author=request.user,
        discussion=discussion
    )
    return comment


# Listar comentários de uma discussão
@router.get("/discussions/{discussion_id}/comments", response=List[CommentOut])
def list_comments(request, discussion_id: int):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    return discussion.comments.all()


# Deletar comentário (somente autor ou admin)
@router.delete("/comments/{comment_id}", auth=auth)
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author and request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    comment.delete()
    return {"message": "Comentário deletado com sucesso"}