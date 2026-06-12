from rest_framework.permissions import BasePermission


class IsCustomerOrOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user.is_authenticated
                and request.user.type == 'customer'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.reviewer == request.user
        return False
