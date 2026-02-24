from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import jwt
from .models import User


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ignore static, index, and weird Chrome devtools probe requests
        if (
            request.path == '/' or
            request.path.startswith('/static/') or
            request.path.startswith('/.well-known/')
        ):
            return None

        # Allow some API endpoints
        if request.path.startswith('/api/') and not request.path.startswith('/api/profile/') and not request.path.startswith('/api/upload/'):
            return None

        # Get token from cookies
        token = request.COOKIES.get('access_token')
        if not token:
            if not request.path.startswith('/api/'):
                return HttpResponseRedirect(reverse('index'))
            return None

        try:
            # ⚠️ Voluntarily vulnerable decode without signature verification
            print(f"Token from cookie: {token}")
            payload = jwt.decode(
                token,
                options={"verify_signature": False, "verify_exp": False},
                algorithms=["HS256", "none"]
            )
            print(f"Decoded JWT payload: {payload}")

            # Attach fake user based on payload only
            class FakeUser:
                def __init__(self, username, role):
                    self.username = username
                    self.role = role

                def __str__(self):
                    return self.username

            request.user = FakeUser(payload.get('username'), payload.get('role'))
            request.jwt_payload = payload

            print(f"Decoded JWT user: {request.user}")
            print(f"User role: {request.user.role}")

            # Allow or block based on role in token
            if request.path.startswith('/admin-panel/') and request.user.role != "admin":
                return HttpResponseRedirect(reverse('dashboard'))

        except Exception as e:
            print(f"[JWT ERROR] {e}")
            return HttpResponseRedirect(reverse('index'))

        return None
