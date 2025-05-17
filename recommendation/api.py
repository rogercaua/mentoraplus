from ninja import Router
from typing import List
from .models import Recommendation
from .schemas import RecommendationIn, RecommendationOut, RecommendationUpdate
from django.shortcuts import get_object_or_404
from datetime import datetime
from user.auth import auth
from ninja.errors import HttpError

router = Router()

@router.post("/", response=RecommendationOut, auth=auth)
def create_recommendation(request, data: RecommendationIn):
    recommendation = Recommendation.objects.create(
        title=data.title,
        description=data.description,
        type=data.type,
        suggested_by=request.user,
        status="pending"
    )
    recommendation = Recommendation.objects.select_related('suggested_by', 'reviewed_by').get(id=recommendation.id)
    return RecommendationOut.from_orm(recommendation)

@router.get("/", response=List[RecommendationOut], auth=auth)
def list_recommendations(request):
    if request.user.role != "admin":
        return []
    qs = Recommendation.objects.select_related('suggested_by', 'reviewed_by').all()
    return [RecommendationOut.from_orm(rec) for rec in qs]



@router.get("/pending", response=List[RecommendationOut], auth=auth)
def list_pending_recommendations(request):
    if request.user.role != "admin":
        raise HttpError(403, "Not authorized")
    qs = Recommendation.objects.select_related('suggested_by', 'reviewed_by').filter(status="pending")
    return [RecommendationOut.from_orm(rec) for rec in qs]



@router.patch("/{rec_id}", response=RecommendationOut, auth=auth)
def update_recommendation(request, rec_id: int, data: RecommendationUpdate):
    if request.user.role != "admin":
        raise HttpError(403, "Not authorized")
    recommendation = get_object_or_404(Recommendation, id=rec_id)
    recommendation.status = data.status
    recommendation.reviewed_by = request.user
    recommendation.updated_at = datetime.now()
    recommendation.save()

    if data.status == "approved":
        from content.models import Content
        Content.objects.create(
            title=recommendation.title,
            description=recommendation.description,
            type=recommendation.type,
            created_by=request.user,
        )
    recommendation = Recommendation.objects.select_related('suggested_by', 'reviewed_by').get(id=rec_id)
    return RecommendationOut.from_orm(recommendation)



@router.get("/{rec_id}", response=RecommendationOut, auth=auth)
def get_recommendation(request, rec_id: int):
    recommendation = get_object_or_404(Recommendation.objects.select_related('suggested_by', 'reviewed_by'), id=rec_id)
    return RecommendationOut.from_orm(recommendation)



@router.patch("/{rec_id}/reject", response=RecommendationOut, auth=auth)
def reject_recommendation(request, rec_id: int):
    if request.user.role != "admin":
        raise HttpError(403, "Not authorized")

    recommendation = get_object_or_404(Recommendation, id=rec_id)
    recommendation.status = "rejected"
    recommendation.reviewed_by = request.user
    recommendation.updated_at = datetime.now()
    recommendation.save()

    recommendation = Recommendation.objects.select_related('suggested_by', 'reviewed_by').get(id=rec_id)
    return RecommendationOut.from_orm(recommendation)



@router.delete("/delete_rejected", auth=auth)
def delete_rejected_recommendations(request):
    if request.user.role != "admin":
        return {"error": "Not authorized"}

    rejected_recommendations = list(Recommendation.objects.filter(status="rejected"))

    deleted_data = [
        {
            "id": rec.id,
            "title": rec.title,
            "description": rec.description,
            "type": rec.type,
            "suggested_by": rec.suggested_by.id if rec.suggested_by else None,
            "status": rec.status,
        }
        for rec in rejected_recommendations
    ]

    Recommendation.objects.filter(status="rejected").delete()

    return {"deleted_recommendations": deleted_data}
