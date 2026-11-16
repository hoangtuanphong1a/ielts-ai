from rest_framework.permissions import BasePermission

from .models import Role


def HasRole(*roles):
    """Tạo permission class chỉ cho phép các vai trò được liệt kê.

    Dùng: permission_classes = [HasRole(Role.ADMIN)]
          permission_classes = [HasRole(Role.TEACHER, Role.ADMIN)]
    """

    class _HasRole(BasePermission):
        message = "You do not have permission to do this."

        def has_permission(self, request, view):
            user = request.user
            if not (user and user.is_authenticated):
                return False
            profile = getattr(user, "profile", None)
            return profile is not None and profile.role in roles

    _HasRole.__name__ = f"HasRole_{'_'.join(roles)}"
    return _HasRole


IsAdminRole = HasRole(Role.ADMIN)
IsTeacherOrAdmin = HasRole(Role.TEACHER, Role.ADMIN)
