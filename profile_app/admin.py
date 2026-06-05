from django.contrib import admin
from profile_app.models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    """
    Administration interface for the Profile model.
    Organizes profile properties into collapsible sections and optimizes
    lookup fields.
    """
    list_display = ('user_username',
                    'email', 'tel', 'location', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('user__username', 'email', 'user__email', 'location')
    readonly_fields = ('created_at', 'uploaded_at')
    fieldsets = (
        ('User Account', {
            'fields': ('user', 'created_at', 'file', 'uploaded_at'),
            'description': 'The primary account linked to this profile.'
        }),
        ('Contact Details', {
            'fields': ('email', 'tel', ),
            'classes': ('collapse',),
        }),
        ('Additional information', {
            'fields': ('location', 'description', 'working_hours'),
            'classes': ('collapse',),
        }),
    )

    def user_username(self, obj):
        """
        Retrieves and displays the username of the related user instance in
        the list view.
        """
        return obj.user.username
    user_username.short_description = 'User'
    user_username.admin_order_field = 'user__username'


admin.site.register(Profile, ProfileAdmin)
