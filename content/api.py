from ninja import Router
from typing import List, Optional
from .models import Content
from .schemas import ContentIn, ContentOut, ContentUpdate
from user.auth import auth
from django.shortcuts import get_object_or_404
from datetime import datetime

router = Router()

@router.post("/", response=ContentOut, auth=auth)
def create_content(request, data: ContentIn):
    """
    Cria um novo conteúdo.

    - Requer usuário autenticado.
    - Campos obrigatórios: title, description, type.
    - Tags são opcionais.
    - O campo created_by é definido automaticamente pelo usuário autenticado.

    Retorna o conteúdo criado.
    """
    content = Content.objects.create(
        title=data.title,
        description=data.description,
        type=data.type,
        tags=data.tags or [],
        created_by=request.user,
    )
    return content

@router.get("/", response=List[ContentOut])
def list_contents(request):
    """
    Lista todos os conteúdos disponíveis.
    """
    return Content.objects.all()

@router.get("/search/", response=List[ContentOut])
def search_contents(request, q: Optional[str] = None):
    """
    Busca conteúdos pelo título.

    - Parâmetro `q`: termo para busca no título (case-insensitive).
    - Se `q` não for informado ou vazio, retorna todos os conteúdos.
    """
    if not q:
        return Content.objects.all()
    return Content.objects.filter(title__icontains=q)

@router.get("/{content_id}", response=ContentOut)
def get_content(request, content_id: int):
    """
    Retorna os detalhes de um conteúdo específico pelo ID.
    """
    content = get_object_or_404(Content, id=content_id)
    return content

@router.put("/{content_id}", response=ContentOut, auth=auth)
def update_content(request, content_id: int, data: ContentUpdate):
    """
    Atualiza um conteúdo existente.

    - Apenas o criador do conteúdo ou um usuário admin podem atualizar.
    - Campos atualizáveis são opcionais, apenas os enviados serão alterados.
    - Atualiza automaticamente o campo updated_at.

    Retorna o conteúdo atualizado.
    """
    content = get_object_or_404(Content, id=content_id)
    if content.created_by != request.user and request.user.role != "admin":
        return {"error": "Not authorized"}
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(content, attr, value)
    content.updated_at = datetime.now()
    content.save()
    return content

@router.delete("/{content_id}", auth=auth)
def delete_content(request, content_id: int):
    """
    Deleta um conteúdo existente.

    - Apenas o criador do conteúdo ou um usuário admin podem deletar.

    Retorna sucesso se deletado.
    """
    content = get_object_or_404(Content, id=content_id)
    if content.created_by != request.user and request.user.role != "admin":
        return {"error": "Not authorized"}
    content.delete()
    return {"success": True}
