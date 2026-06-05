from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auth_app.models import User

# Register your models here.


class UserAdmin(UserAdmin):
    """
    Custom administration interface for the User model.
    Extends standard Django UserAdmin to integrate and manage the custom
    'type' role field.
    """
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'type', 'is_staff')
    list_filter = ('type', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_editable = ('type',)
    fieldsets = UserAdmin.fieldsets + (
        ('Account type', {
            'fields': ('type',),
            'description': 'Determines the user role in the system '
            '(customer or business customer).'
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Account type', {
            'fields': ('type',),
        }),
    )


admin.site.register(User, UserAdmin)
