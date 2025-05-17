from django.urls import path
from .api import api  # Ajuste o import conforme sua estrutura

urlpatterns = [
    path("api/", api.urls),
]
