from rest_framework.permissions import BasePermission


class IsBusinessOrOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user.is_authenticated
        if request.method == 'POST':
            return (
                request.user.is_authenticated
                and request.user.type == 'business'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.user == request.user
        return True
