from rest_framework import permissions


class ReviewCommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'DELETE'):
            return (request.user == obj.author or
                    request.user.is_admin or
                    request.user.is_moderator)

        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminOrDjangoAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in (
                'POST', 'DELETE', 'PATCH') and request.user.is_authenticated:
            return request.user.is_admin
        return request.method == 'GET'
