from ninja.security import HttpBearer
from jose import jwt
from django.conf import settings
from user.models import User

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["sub"])
            request.user = user
            return token
        except Exception:
            return None

auth = AuthBearer()
