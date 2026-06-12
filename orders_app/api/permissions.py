from rest_framework.permissions import BasePermission


class IsBusinessOrOwnerOrCustomer(BasePermission):
    """
    Custom permission class to control access to orders.
    - Creation (POST) is restricted strictly to authenticated customers.
    - Global view access requires standard authentication.
    - Instance access is limited based on HTTP methods (Owners/Staff).
    """

    def has_permission(self, request, view):
        """Check global permissions for incoming list or creation requests."""
        if request.method == 'POST':
            return (
                request.user.is_authenticated
                and request.user.type == 'customer'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check object-level permissions for specific order instances."""
        if request.method == 'GET':
            return (
                obj.customer_user == request.user
                or obj.business_user == request.user
            )
        if request.method == 'PATCH':
            return obj.business_user == request.user
        if request.method == 'DELETE':
            return request.user.is_staff
        return False
