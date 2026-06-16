from django.contrib import admin
from django import forms
from .models import Offer, OfferDetail


class OfferDetailFormSet(forms.models.BaseInlineFormSet):
    """
    Custom inline formset for managing OfferDetail form instances.
    Enforces cross-form validation rules to ensure unique package type
    allocations within a single parent offer workspace.
    """

    def clean(self):
        """
        Validate that package types are unique across all sub-forms.
        Bypasses forms slated for deletion or completely unchanged extra forms.
        """
        super().clean()
        prefix = self.prefix
        seen_types = {}
        for i, form in enumerate(self.forms):
            if self.data.get(f'{prefix}-{i}-DELETE') or (
                    self.can_delete and self._should_delete_form(form)):
                continue
            offer_type = self.data.get(f'{prefix}-{i}-offer_type')
            if offer_type:
                val_str = str(offer_type).lower().strip()
                if val_str in seen_types:
                    error_msg = f"The package type '{offer_type}' may only exist once per offer."
                    form.add_error('offer_type', error_msg)
                else:
                    seen_types[val_str] = form


class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    formset = OfferDetailFormSet
    extra = 3
    max_num = 3
    fields = ('offer_type', 'title', 'price',
              'delivery_time_in_days', 'revisions', 'features')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'min_price', 'min_delivery_time')
    list_filter = ("user", 'title',)
    search_fields = ("id", "title", "user__username", "user__email")
    ordering = ("-id",)
    inlines = [OfferDetailInline]


admin.site.register(Offer, OfferAdmin)
