from ninja import Router
from typing import List, Optional
from user.auth import auth
from mentoraplus.responses import MessageOut
from .models import Recommendation, Content
from .schemas import RecommendationIn, RecommendationOut
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

router = Router(tags=["Recommendation"])

# ADMIN - listar todas as recomendações
@router.get("/recommendations", response=List[RecommendationOut], auth=auth)
def list_all_recommendations(request):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    
    recs = Recommendation.objects.all()
    return recs

#----------------------------------------------------------------------------------------->

# USUÁRIO - criar recomendação (tags capitalizadas)
@router.post("/recommendations", response=RecommendationOut, auth=auth)
def create_recommendation(request, data: RecommendationIn):
    data.tags = [tag.capitalize() for tag in data.tags] if hasattr(data, 'tags') else []
    
    rec = Recommendation.objects.create(
        title=data.title,
        description=data.description,
        type=data.type,
        url=data.url,
        tags=data.tags,
        status="pending",
        suggested_by=request.user,
    )
    return rec

#----------------------------------------------------------------------------------------->

# ADMIN - deletar recomendação pelo ID
@router.delete("/recommendations/{rec_id}", response=MessageOut, auth=auth)
def delete_recommendation(request, rec_id: int):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    
    rec = get_object_or_404(Recommendation, id=rec_id)

    rec.delete()
    return {"message": "Recomendação deletada com sucesso"}

#----------------------------------------------------------------------------------------->

# ADMIN - listar recomendações pendentes
@router.get("/recommendations/pending", response=List[RecommendationOut], auth=auth)
def list_pending_recommendations(request):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    
    recs = Recommendation.objects.filter(status="pending")
    return recs

#----------------------------------------------------------------------------------------->

# ADMIN - aprovar recomendação: muda status para aprovado e adiciona em Content
@router.post("/recommendations/{rec_id}/approve", response=MessageOut, auth=auth)
def approve_recommendation(request, rec_id: int):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    
    rec = get_object_or_404(Recommendation, id=rec_id)
    
    if rec.status != "pending":
        raise HttpError(400, "Recomendação não está pendente")
    
    rec.status = "approved"
    rec.reviewed_by = request.user
    rec.save()

    Content.objects.create(
        title=rec.title,
        description=rec.description,
        type=rec.type,
        url=rec.url,
        created_by=rec.suggested_by,
        tags=rec.tags
    )
    return {"message": "Recomendação aprovada e conteúdo criado"}

#----------------------------------------------------------------------------------------->

# ADMIN - rejeitar recomendação (com opção de deletar)
@router.post("/recommendations/{rec_id}/reject", auth=auth)
def reject_recommendation(request, rec_id: int):
    if request.user.role != "admin":
        raise HttpError(403, "Não autorizado")
    rec = get_object_or_404(Recommendation, id=rec_id)
    if rec.status != "pending":
        raise HttpError(400, "Recomendação não está pendente")

    rec.status = "rejected"
    rec.reviewed_by = request.user
    rec.save()
    
    return {"message": "Recomendação rejeitada"}
