from ninja import Router
from typing import List, Optional
from user.auth import auth
from .models import Content
from .schemas import ContentIn, ContentOut
from mentoraplus.responses import MessageOut
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

router = Router(tags=["Content"])

# Listar todos os conteúdos (user e admin)
@router.get("/contents", response=List[ContentOut], auth=auth)
def list_contents(request, tag: Optional[str] = None, type: Optional[str] = None):
    query = Content.objects.all()
    
    if tag:
        query = query.filter(tags__icontains=tag.capitalize())
    if type:
        query = query.filter(type=type)
        
    return query

# Listar todas as tags (únicas) já existentes nos conteúdos
@router.get("/contents/tags", auth=auth)
def list_tags(request):
    tags_set = set()
    for content in Content.objects.all():
        tags_set.update(content.tags)
    return {"tags": sorted(tags_set)}

# Deletar conteúdo (admin)
@router.delete("/contents/{content_id}", auth=auth)
def delete_content(request, content_id: int):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    content = get_object_or_404(Content, id=content_id)
    content.delete()
    return {"message": "Conteúdo deletado com sucesso"}

# Adicionar conteúdo (admin), capitalizando tags
@router.post("/contents", response=ContentOut, auth=auth)
def add_content(request, data: ContentIn):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    
    data.tags = [tag.upper() for tag in data.tags] if hasattr(data, 'tags') else []
    
    content = Content.objects.create(
        title=data.title,
        description=data.description,
        type=data.type,
        url=data.url,
        created_by=request.user,
        tags=data.tags
    )
    return content

# Atualizar conteúdo (admin)
@router.put("/contents/{content_id}", response=ContentOut, auth=auth)
def update_content(request, content_id: int, data: ContentIn):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    content = get_object_or_404(Content, id=content_id)
    content.title = data.title
    content.description = data.description
    content.type = data.type
    content.url = data.url
    content.tags = [tag.upper() for tag in data.tags]
    content.save()
    
    return content
