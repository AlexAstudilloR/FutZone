from rest_framework.permissions import BasePermission, SAFE_METHODS
from profiles.models import ProfileModel


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return getattr(user, "is_admin", False)


class IsAdminOrOwnerWithLimitedEdit(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        profile = request.user
        is_admin = getattr(profile, "is_admin", False)
        is_owner = obj.user_id == profile.id

        if request.method in SAFE_METHODS:
            return is_admin or is_owner
        if request.method == "POST":
            return True
        if is_admin and not is_owner and set(request.data.keys()) <= {"status"}:
            return True
        return is_owner
