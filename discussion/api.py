from ninja import Router
from typing import List
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from .models import Discussion
from .schemas import DiscussionIn, DiscussionOut
from mentoraplus.responses import MessageOut
from content.models import Content
from user.auth import auth

router = Router(tags=["Discussion"])

# Criar uma discussão
@router.post("/discussions", response=DiscussionOut, auth=auth)
def create_discussion(request, data: DiscussionIn):
    content = get_object_or_404(Content, id=data.related_content_id)
    discussion = Discussion.objects.create(
        title=data.title,
        content=data.content,
        related_content=content,
        author=request.user
    )
    return discussion

#----------------------------------------------------------------------------------------->

# Listar todas as discussões
@router.get("/discussions", response=List[DiscussionOut])
def list_discussions(request):
    return Discussion.objects.all()

#----------------------------------------------------------------------------------------->

# Listar discussões de um conteúdo específico
@router.get("/discussions/content/{content_id}", response=List[DiscussionOut])
def list_discussions_by_content(request, content_id: int):
    content = get_object_or_404(Content, id=content_id)
    return content.discussions.all()

#----------------------------------------------------------------------------------------->

# Fechar uma discussão (somente o autor ou admin)
@router.post("/discussions/{discussion_id}/close", response=MessageOut, auth=auth)
def close_discussion(request, discussion_id: int):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if request.user != discussion.author and request.user.role != "admin":
        raise HttpError(403, "Não autorizado")

    discussion.is_closed = True
    discussion.save()
    return {"message": "Discussão fechada com sucesso"}


# Deletar uma discussão (somente autor ou admin)
@router.delete("/discussions/{discussion_id}", response=MessageOut, auth=auth)
def delete_discussion(request, discussion_id: int):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if request.user != discussion.author and request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    discussion.delete()
    return {"message": "Discussão deletada com sucesso"}