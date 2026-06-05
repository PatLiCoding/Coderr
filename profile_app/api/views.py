from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from auth_app.models import User
from profile_app.models import Profile
from profile_app.api.serializers import ProfilDetailSerializer, \
    BusinessSerializer, CustomerSerializer
from profile_app.api.permissions import IsProfilOwner


class ProfilDetailView(RetrieveUpdateAPIView):
    """
    API view to retrieve or update a specific user's profile.
    Automatically creates a profile if one doesn't exist for a valid user.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfilDetailSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions required for
        this view.
        Requires object ownership for PATCH updates; standard authentication
        otherwise.
        """
        if self.request.method == 'PATCH':
            return [IsProfilOwner()]
        return [IsAuthenticated()]

    def get_object(self):
        """
        Fetches the profile linked to the user requested via URL parameters.
        Raises a NotFound error if the user does not exist.
        """
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")
        profil, created = Profile.objects.get_or_create(user=user)
        self.check_object_permissions(self.request, profil)
        return profil


class BusinessListView(ListAPIView):
    """
    API endpoint that lists all user profiles classified as
    'business' accounts.
    """
    queryset = Profile.objects.filter(user__type='business').distinct()
    serializer_class = BusinessSerializer


class CustomerListView(ListAPIView):
    """
    API endpoint that lists all user profiles classified as
    'customer' accounts.
    """
    queryset = Profile.objects.filter(user__type='customer').distinct()
    serializer_class = CustomerSerializer
