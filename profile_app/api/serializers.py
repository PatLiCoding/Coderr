from rest_framework import serializers
from django.core.files.storage import default_storage
from profile_app.models import Profile


class ProfilDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for complete profile management.
    Handles nested, writeable user account data updates alongside
    profile fields.
    """
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    type = serializers.ReadOnlyField(source='user.type')
    first_name = serializers.CharField(
        source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(
        source='user.last_name', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at'
        ]

    def update(self, instance, validated_data):
        """
        Overrides standard update flow to cleanly process separated
        nested user info and custom profile file storage logic.
        """
        user_data = validated_data.pop('user', None)
        uploaded_file = validated_data.pop('file', None)
        if user_data:
            self._update_user(instance.user, user_data)
        instance = super().update(instance, validated_data)
        if uploaded_file:
            self._handle_file(instance, uploaded_file)
        return instance

    def _update_user(self, user, user_data):
        """
        Helper method to iterate and save updated fields onto the associated
        User model.
        """
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

    def _handle_file(self, instance, uploaded_file):
        """
        Helper method managing storage cleanups and generating clean,
        user-isolated file system paths for uploaded files.
        """
        if instance.file and default_storage.exists(instance.file.name):
            default_storage.delete(instance.file.name)
        ext = uploaded_file.name.split('.')[-1]
        custom_path = f'uploads/user_{instance.user.id}/profile.{ext}'
        uploaded_file.name = custom_path
        instance.file = uploaded_file
        instance.save()


class BusinessSerializer(serializers.ModelSerializer):
    """
    Public exposure serializer optimized for showcasing specific
    'business' profile cards.
    """
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    type = serializers.ReadOnlyField(source='user.type')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    """
    Lightweight exposure serializer optimized for high-level
    'customer' listings.
    """
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    type = serializers.ReadOnlyField(source='user.type')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'uploaded_at', 'type'
        ]
