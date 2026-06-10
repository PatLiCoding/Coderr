from rest_framework.generics import ListCreateAPIView
# RetrieveAPIView, \ RetrieveUpdateDestroyAPIView
from django.db.models import Q
from orders_app.api.serializers import OrdersSerializer
from orders_app.models import Order
from orders_app.api.permissions import IsBusinessOrOwnerOrCustomer


class OrdersView(ListCreateAPIView):
    serializer_class = OrdersSerializer
    queryset = Order.objects.all()
    permission_classes = [IsBusinessOrOwnerOrCustomer]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) |
            Q(business_user=user)
        )
