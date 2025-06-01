from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jose import jwt, JWTError, ExpiredSignatureError
from profiles.models import ProfileModel
from django.conf import settings
import hashlib
import time
from threading import Lock


_token_cache = {}
_user_cache = {}
_cache_lock = Lock()
TOKEN_CACHE_DURATION = 300  
USER_CACHE_DURATION = 600   

class SupabaseRemoteAuth(BaseAuthentication):

    def _get_token_hash(self, token):
        return hashlib.md5(token.encode()).hexdigest()

    def _get_cached_token(self, token_hash):
        with _cache_lock:
            if token_hash in _token_cache:
                cached_data, timestamp = _token_cache[token_hash]
                if time.time() - timestamp < TOKEN_CACHE_DURATION:
                    return cached_data
                else:
                    del _token_cache[token_hash]
        return None

    def _cache_token(self, token_hash, decoded_data):
        with _cache_lock:
            _token_cache[token_hash] = (decoded_data, time.time())

    def _get_cached_user(self, user_id):
        with _cache_lock:
            if user_id in _user_cache:
                cached_data, timestamp = _user_cache[user_id]
                if time.time() - timestamp < USER_CACHE_DURATION:
                    return cached_data
                else:
                    del _user_cache[user_id]
        return None

    def _cache_user(self, user_id, user):
        with _cache_lock:
            _user_cache[user_id] = (user, time.time())

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        token_hash = self._get_token_hash(token)

        decoded = self._get_cached_token(token_hash)

        if decoded is None:
            try:
                decoded = jwt.decode(
                    token,
                    settings.SUPABASE_JWT_SECRET.strip(),
                    algorithms=["HS256"],
                    options={"verify_aud": False}
                )
                self._cache_token(token_hash, decoded)
            except ExpiredSignatureError:
                raise AuthenticationFailed("Token expirado")
            except JWTError:
                raise AuthenticationFailed("Token inválido")

        user_id = decoded.get("sub")
        if not user_id:
            raise AuthenticationFailed("Token sin ID de usuario")

        user = self._get_cached_user(user_id)

        if user is None:
            try:
                user, _ = ProfileModel.objects.get_or_create(
                    id=user_id,
                    defaults={
                        "email": decoded.get("email") or decoded.get("user_metadata", {}).get("email")
                    }
                )
                self._cache_user(user_id, user)
            except Exception:
                raise AuthenticationFailed("Error al procesar usuario")

        return (user, None)


def clear_auth_cache():
    """Limpia todo el cache de autenticación"""
    global _token_cache, _user_cache
    with _cache_lock:
        _token_cache.clear()
        _user_cache.clear()
