from rest_framework.permissions import BasePermission


class IsBusinessOrOwner(BasePermission):
    """
    Custom permission class to restrict access based on user type and
    ownership.

    Rules:
        - View-level (has_permission):
            - GET: Allowed for any authenticated user.
            - POST: Allowed only for authenticated users with type 'business'.
            - Other methods: Allowed for any authenticated user.
        - Object-level (has_object_permission):
            - PATCH/DELETE: Allowed only if the authenticated user is the
            owner of the object.
            - Other methods (GET/PUT etc.): Allowed.
    """

    def has_permission(self, request, view):
        """Check view-level permissions.

        Args:
            request (HttpRequest): The incoming request instance.
            view (View): The target view class instance.

        Returns:
            bool: True if the request is permitted, False otherwise.
        """
        if request.method in ['GET']:
            return request.user.is_authenticated
        if request.method == 'POST':
            return (
                request.user.is_authenticated
                and request.user.type == 'business'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check object-level permissions for sensitive methods.

        Args:
            request (HttpRequest): The incoming request instance.
            view (View): The target view class instance.
            obj (Model): The model instance being accessed.

        Returns:
            bool: True if the user owns the object or uses a safe method,
            False otherwise.
        """
        if request.method in ['PATCH', 'DELETE']:
            return obj.user == request.user
        return True
