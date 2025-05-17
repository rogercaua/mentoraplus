from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import Discussion
from .schemas import DiscussionIn, DiscussionOut
from user.auth import auth  # seu sistema de autenticação JWT

router = Router()

@router.post("/", response=DiscussionOut, auth=auth)
def create_discussion(request, data: DiscussionIn):
    """
    Cria uma nova discussão.

    - Requer usuário autenticado.
    - Campos obrigatórios: title, content, related_content_id.
    - O autor será o usuário autenticado.

    Retorna a discussão criada.
    """
    discussion = Discussion.objects.create(
        title=data.title,
        content=data.content,
        related_content_id=data.related_content_id,
        author=request.user
    )
    return discussion

@router.get("/{discussion_id}", response=DiscussionOut)
def get_discussion(request, discussion_id: int):
    """
    Retorna os detalhes de uma discussão específica pelo ID.
    """
    discussion = get_object_or_404(Discussion, id=discussion_id)
    return discussion

@router.get("/", response=List[DiscussionOut])
def list_discussions(request):
    """
    Lista todas as discussões.
    """
    return Discussion.objects.all()

@router.put("/{discussion_id}", response=DiscussionOut, auth=auth)
def update_discussion(request, discussion_id: int, data: DiscussionIn):
    """
    Atualiza uma discussão existente.

    - Apenas o autor pode atualizar.
    - Campos atualizáveis: title, content, related_content_id.

    Retorna a discussão atualizada.
    """
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if discussion.author != request.user:
        return {"detail": "Não autorizado."}
    discussion.title = data.title
    discussion.content = data.content
    discussion.related_content_id = data.related_content_id
    discussion.save()
    return discussion

@router.delete("/{discussion_id}", auth=auth)
def delete_discussion(request, discussion_id: int):
    """
    Deleta uma discussão existente.

    - Apenas o autor pode deletar.

    Retorna sucesso se deletado.
    """
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if discussion.author != request.user:
        return {"detail": "Não autorizado."}
    discussion.delete()
    return {"success": True}
