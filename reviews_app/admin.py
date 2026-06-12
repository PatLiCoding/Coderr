from django.contrib import admin
from reviews_app.models import Review


class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Review model.
    Organizes layout structure into structured fieldsets, registers filters,
    and displays a dynamic star rating helper column.
    """
    list_display = ('id', 'reviewer', 'business_user',
                    'rating_stars', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'updated_at')
    search_fields = ('reviewer__username',
                     'business_user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Individuals involved', {
            'fields': ('reviewer', 'business_user')
        }),
        ('Review content', {
            'fields': ('rating', 'description')
        }),
        ('System timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def rating_stars(self, obj):
        """
        Convert the integer rating field into a visual 5-star text indicator.
        """
        return "★" * obj.rating + "☆" * (5 - obj.rating)


admin.site.register(Review, ReviewAdmin)
