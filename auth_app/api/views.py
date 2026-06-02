
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from auth_app.models import User
from auth_app.api.serializers import UserSerializer, LoginSerializer


class RegistrationView(CreateAPIView):
    """
    Generic view for user registration.
    Allows unauthenticated users to create a new user profile using
    the UserSerializer.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(CreateAPIView):
    """
    Generic view for user login.
    Expects username and password, validates the credentials,
    and returns an authentication token along with basic user details.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id
        }, status=status.HTTP_200_OK)
