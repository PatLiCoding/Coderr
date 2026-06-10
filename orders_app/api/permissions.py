from rest_framework.permissions import BasePermission


class IsBusinessOrOwnerOrCustomer(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user.is_authenticated
                and request.user.type == 'customer'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return (
                obj.customer_user == request.user
                or obj.business_user == request.user
            )

        if request.method in ['PATCH', 'DELETE']:
            return obj.business_user == request.user

        return False
