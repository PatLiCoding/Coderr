from rest_framework.permissions import BasePermission


class IsProfilOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return obj.user == request.user
