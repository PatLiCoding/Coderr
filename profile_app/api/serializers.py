from rest_framework import serializers
from django.core.files.storage import default_storage
from profile_app.models import Profile


class ProfilDetailSerializer(serializers.ModelSerializer):
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
        user_data = validated_data.pop('user', None)
        uploaded_file = validated_data.pop('file', None)
        if user_data:
            self._update_user(instance.user, user_data)
        instance = super().update(instance, validated_data)
        if uploaded_file:
            self._handle_file(instance, uploaded_file)
        return instance

    def _update_user(self, user, user_data):
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

    def _handle_file(self, instance, uploaded_file):
        if instance.file and default_storage.exists(instance.file.name):
            default_storage.delete(instance.file.name)
        ext = uploaded_file.name.split('.')[-1]
        custom_path = f'uploads/user_{instance.user.id}/profile.{ext}'
        instance.file = default_storage.save(custom_path, uploaded_file)
        instance.save(update_fields=['file'])


class BusinessSerializer(serializers.ModelSerializer):
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
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    type = serializers.ReadOnlyField(source='user.type')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'type'
        ]
