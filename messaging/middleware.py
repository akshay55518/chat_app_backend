import jwt
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token")
        user = None

        if token:
            try:
                decoded = jwt.decode(
                    token[0],
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )
                user = await get_user(decoded.get("user_id"))
            except Exception:
                user = None

        scope["user"] = user

        return await self.app(scope, receive, send)