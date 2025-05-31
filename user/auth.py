from ninja.security import HttpBearer
from jose import jwt, JWTError
from django.conf import settings
from user.models import User

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('sub')
            if user_id is None:
                return None
            user = User.objects.get(id=user_id)
            request.user = user
            return token
        except (JWTError, User.DoesNotExist):
            return None

auth = AuthBearer()