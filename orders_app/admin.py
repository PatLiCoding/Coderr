from django.contrib import admin
from orders_app.api.permissions import IsBusinessOrOwnerOrCustomer
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Handles custom permissions, dynamic fieldsets, form adjustments,
    and displays read-only related offer information.
    """
    list_display = (
        "id", "customer_user", "business_user", "get_offer_title",
        "status", "created_at", "updated_at", )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("id", "customer_user__username",
                     "business_user__username", "offer_detail__title",)
    ordering = ("-created_at",)

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Override the default form to change the label of the
        'offer_detail' field.
        """
        form = super().get_form(request, obj, change, **kwargs)
        if 'offer_detail' in form.base_fields:
            form.base_fields['offer_detail'].label = "Offer"
        return form

    def has_change_permission(self, request, obj=None):
        """
        Determine if the user has permission to change/edit the order.
        Superusers always have access; otherwise, validation is delegated
        to the custom API permission class.
        """
        if request.user.is_superuser:
            return True
        permission = IsBusinessOrOwnerOrCustomer()
        if obj is None:
            return permission.has_permission(request, view=None)
        return permission.has_object_permission(request, view=None, obj=obj)

    def has_delete_permission(self, request, obj=None):
        """
        Restrict order deletion strictly to staff members.
        """
        return request.user.is_staff

    def has_add_permission(self, request):
        """
        Only allow superusers or users of type 'customer' to manually create
        an order.
        """
        if request.user.is_superuser:
            return True
        return request.user.type == 'customer'

    def get_readonly_fields(self, request, obj=None):
        """
        Make core order attributes and nested offer details read-only
        once created.
        """
        if obj:
            return ("id",
                    "customer_user", "business_user", "created_at",
                    "updated_at", "get_offer_title", "get_offer_revisions",
                    "get_offer_delivery_time", "get_offer_price",
                    "get_offer_features", "get_offer_type"
                    )
        return ()

    def get_fieldsets(self, request, obj=None):
        """
        Dynamically structure the layout based on whether an order is being
        created or viewed.
        """
        if not obj:
            return (
                ('New Order', {
                    'fields': ("offer_detail",),
                }),
            )
        return (
            ('Order Details', {
                'fields': ("id", "customer_user", "business_user",
                           "status", "created_at", "updated_at"),
            }),
            ('Offer Details', {
                'fields': ("get_offer_title", "get_offer_revisions",
                           "get_offer_delivery_time", "get_offer_price",
                           "get_offer_features", "get_offer_type"),
            }),
        )

    def save_model(self, request, obj, form, change):
        """
        Automatically assign the current user as the customer and
        derive the business user from the linked offer when creating a
        new order.
        """
        if not change:
            obj.customer_user = request.user
            if obj.offer_detail and obj.offer_detail.offer:
                obj.business_user = obj.offer_detail.offer.user
        super().save_model(request, obj, form, change)

    @admin.display(description='Title')
    def get_offer_title(self, obj):
        """
        Retrieve the title of the associated offer detail.
        """
        return obj.offer_detail.title if obj.offer_detail else "-"

    @admin.display(description='Revisions')
    def get_offer_revisions(self, obj):
        """
        Retrieve the number of revisions allowed for the associated
        offer detail.
        """
        return obj.offer_detail.revisions if obj.offer_detail else "-"

    @admin.display(description='Delivery Time (Days)')
    def get_offer_delivery_time(self, obj):
        """
        Retrieve the delivery time in days for the associated offer detail.
        """
        return (obj.offer_detail.delivery_time_in_days
                if obj.offer_detail else "-")

    @admin.display(description='Price')
    def get_offer_price(self, obj):
        """
        Retrieve the price of the associated offer detail.
        """
        return obj.offer_detail.price if obj.offer_detail else "-"

    @admin.display(description='Features')
    def get_offer_features(self, obj):
        """
        Retrieve the structured features list for the associated offer detail.
        """
        return obj.offer_detail.features if obj.offer_detail else "-"

    @admin.display(description='Type')
    def get_offer_type(self, obj):
        """
        Retrieve the pricing tier/type (e.g., basic) of the associate
        offer detail.
        """
        return obj.offer_detail.offer_type if obj.offer_detail else "-"


admin.site.register(Order, OrderAdmin)
