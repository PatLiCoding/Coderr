from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from auth_app.models import User
from profile_app.models import Profile
from profile_app.api.serializers import ProfilDetailSerializer
from profile_app.api.permissions import IsProfilOwner


class ProfilDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilDetailSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsProfilOwner()]
        return [IsAuthenticated()]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")
        profil, created = Profile.objects.get_or_create(user=user)
        self.check_object_permissions(self.request, profil)
        return profil
