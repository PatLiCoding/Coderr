from django.contrib import admin
from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """
    Allows the OfferDetails to be displayed and edited directly within the
    edit view of the parent offer.
    """
    model = OfferDetail
    extra = 0
    fields = ('offer_type', 'title', 'price',
              'delivery_time_in_days', 'revisions', 'features')
    classes = ('collapse',)

    def has_add_permission(self, request, obj=None):
        """Completely disables the 'Add another item' button."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Removes the checkbox for deleting existing details."""
        return False


class OfferAdmin(admin.ModelAdmin):
    """
    Configuration for the main offer.
    """
    list_display = ('id', 'title', 'user', 'min_price', 'min_delivery_time')
    list_display_links = ('id', 'title')
    list_filter = ('min_delivery_time', 'user')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    inlines = [OfferDetailInline]


admin.site.register(Offer, OfferAdmin)
