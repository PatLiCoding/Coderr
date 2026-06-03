from rest_framework import serializers
from django.core.files.storage import default_storage
from profile_app.models import Profile


class ProfilDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    type = serializers.ReadOnlyField(source='user.type')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at'
        ]

    def save(self, **kwargs):
        uploaded_file = self.validated_data.pop('file', None)
        instance = super().save(**kwargs)
        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1]
            custom_path = f'uploads/user_{instance.user.id}/profile.{ext}'
            if instance.file and default_storage.exists(instance.file.name):
                default_storage.delete(instance.file.name)
            actual_path = default_storage.save(custom_path, uploaded_file)
            instance.file = actual_path
            instance.save(update_fields=['file'])
        return instance

    def get_first_name(self, obj):
        return obj.user.first_name or ''

    def get_last_name(self, obj):
        return obj.user.last_name or ''

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['file']:
            data['file'] = ''
        return data
