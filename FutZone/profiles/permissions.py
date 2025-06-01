from rest_framework.permissions import BasePermission, SAFE_METHODS
from profiles.models import ProfileModel

class IsAdminOrReadOnly(BasePermission):
    """
    Permite lectura a usuarios autenticados, y acceso total solo a administradores
    definidos por el campo 'is_admin' en Supabase.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        try:
            profile = ProfileModel.objects.get(id=request.user.id)
            return profile.is_admin
        except ProfileModel.DoesNotExist:
            return False
