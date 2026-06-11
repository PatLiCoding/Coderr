from rest_framework.test import APITestCase
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from auth_app.models import User
from orders_app.models import Order
from orders_app.admin import OrderAdmin
from offers_app.models import Offer, OfferDetail


class OdersTestsHappyPath(APITestCase):
    """
    Test suite for the custom OrderAdmin panel functionality.
    Verifies that permissions, model saving logic, fieldsets,
    and custom getter fields operate as expected.
    """

    def setUp(self):
        """
        Set up mock admin environment, request factory, users, and
        base models.
        """
        self.site = AdminSite()
        self.admin_instance = OrderAdmin(Order, self.site)
        self.request_factory = RequestFactory()
        self.customer = User.objects.create_user(
            username="customer_user", password="pwd", type="customer")
        self.business_user = User.objects.create_user(
            username="business_user", password="pwd", type="business")
        self.superuser = User.objects.create_superuser(
            username="admin_user", password="pwd", email="admin@test.com")
        self.offer = Offer.objects.create(
            user=self.business_user, title="Mein tolles Angebot",
            description="Eine detaillierte Beschreibung")
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer, title="Basic Paket", revisions=3,
            delivery_time_in_days=5, price=49.99,
            features=["Feature 1", "Feature 2"], offer_type="basic")
        self.order = Order.objects.create(
            customer_user=self.customer, business_user=self.business_user,
            offer_detail=self.offer_detail, status="in_progress")

    def test_order_admin_save_model(self):
        """
        Ensure save_model auto-populates the customer and related business
        user on creation.
        """
        request = self.request_factory.post('/admin/orders_app/order/add/')
        request.user = self.customer
        new_order = Order(offer_detail=self.offer_detail)
        self.admin_instance.save_model(
            request, obj=new_order, form=None, change=False)
        assert new_order.customer_user == self.customer
        assert new_order.business_user == self.business_user

    def test_permissions_as_customer(self):
        """
        Ensure a user with a 'customer' type has permission to add and
        change orders.
        """
        request = self.request_factory.get('/admin/')
        request.user = self.customer
        assert self.admin_instance.has_add_permission(request) is True
        assert self.admin_instance.has_change_permission(
            request, obj=None) is True

    def test_permissions_as_superuser(self):
        """
        Ensure a superuser has full access to add, change, and delete
        order instances.
        """
        request = self.request_factory.get('/admin/')
        request.user = self.superuser
        assert self.admin_instance.has_change_permission(
            request, obj=self.order) is True
        assert self.admin_instance.has_delete_permission(
            request, obj=self.order) is True
        assert self.admin_instance.has_add_permission(request) is True

    def test_dynamic_fields_creation_mode(self):
        """
        Ensure fieldsets and readonly fields are correct in creation mode.
        """
        request = self.request_factory.get('/admin/')
        request.user = self.superuser
        readonly = self.admin_instance.get_readonly_fields(request, obj=None)
        fieldsets = self.admin_instance.get_fieldsets(request, obj=None)
        self.assertIn("offer_detail", fieldsets[0][1]['fields'])
        self.assertEqual(len(readonly), 0)

    def test_dynamic_fields_edit_mode(self):
        """
        Ensure fieldsets and readonly fields are correct in edit mode.
        """
        request = self.request_factory.get('/admin/')
        request.user = self.superuser
        readonly = self.admin_instance.get_readonly_fields(
            request, obj=self.order)
        fieldsets = self.admin_instance.get_fieldsets(request, obj=self.order)
        self.assertIn("get_offer_title", readonly)
        self.assertIn("get_offer_title", fieldsets[1][1]['fields'])

    def test_get_form_label_override(self):
        """
        Ensure the 'offer_detail' form field label is successfully overridden
        to 'Offer'.
        """
        request = self.request_factory.get('/admin/')
        request.user = self.superuser
        form = self.admin_instance.get_form(request, obj=None, change=False)
        assert form.base_fields['offer_detail'].label == "Offer"

    def test_all_offer_detail_getters(self):
        """
        Ensure the custom admin display getters correctly map values from the
        underlying offer detail.
        """
        assert self.admin_instance.get_offer_title(self.order) == "Basic Paket"
        assert self.admin_instance.get_offer_revisions(self.order) == 3
        assert self.admin_instance.get_offer_delivery_time(self.order) == 5
        assert self.admin_instance.get_offer_price(self.order) == 49.99
        assert self.admin_instance.get_offer_features(
            self.order) == ["Feature 1", "Feature 2"]
        assert self.admin_instance.get_offer_type(self.order) == "basic"
