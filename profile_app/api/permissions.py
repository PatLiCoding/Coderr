from rest_framework.permissions import BasePermission


class IsProfilOwner(BasePermission):
    """
    Permission class to restrict object access exclusively to the owner.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the profile object.

        Allows access (True) for PATCH requests only if the profile
        belongs to the currently authenticated user.
        """
        if request.method == 'PATCH':
            return obj.user == request.user
