from rest_framework.permissions import BasePermission, SAFE_METHODS
from profiles.models import ProfileModel


class IsAdminOrReadOnly(BasePermission):
    """
    Lectura a usuarios autenticados,
    escritura solo a administradores
    (request.user.is_admin).
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return getattr(user, 'is_admin', False)

class IsAdminOrOwnerWithLimitedEdit(BasePermission):
    """
    Permiso personalizado para reservas (Appointment).
    - Usuarios autenticados pueden ver y crear sus reservas.
    - Admin puede ver todas, y editar solo 'status' de reservas ajenas.
    """

    def has_permission(self, request, view):
        # Solo usuarios autenticados
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            profile = ProfileModel.objects.get(user=request.user)
        except ProfileModel.DoesNotExist:
            return False

        is_admin = profile.is_admin
        is_owner = obj.user == profile


        if request.method in SAFE_METHODS:
            return is_admin or is_owner


        if request.method == 'POST':
            return True


        if is_admin and not is_owner:

            if set(request.data.keys()) <= {'status'}:
                return True
            return False


        return False
