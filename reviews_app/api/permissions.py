from rest_framework.permissions import BasePermission


class IsCustomerOrOwner(BasePermission):
    """
    Custom permission class to secure review endpoints.
    - Creating a review (POST) is strictly restricted to authenticated users
        of type 'customer'.
    - Listing or viewing reviews (GET) is open to any authenticated user.
    - Modifying or deleting a review (PATCH, DELETE) is exclusively reserved
        for the original author (reviewer).
    """

    def has_permission(self, request, view):
        """
        Check global access controls based on the HTTP method and user type.
        """
        if request.method == 'POST':
            return (
                request.user.is_authenticated
                and request.user.type == 'customer'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check object-level access controls to ensure only owners can alter or
        remove records.
        """
        if request.method in ['PATCH', 'DELETE']:
            return obj.reviewer == request.user
        return False
