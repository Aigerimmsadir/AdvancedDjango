from rest_framework.permissions import IsAuthenticated


class IsAdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.profile.role in [0, 1]


class IsSuperAdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.profile.role == 0
