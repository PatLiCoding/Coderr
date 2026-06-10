from rest_framework.generics import ListCreateAPIView
# RetrieveAPIView, \ RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from orders_app.api.serializers import OrderSerializer, OrderCreateSerializer
from orders_app.models import Order
from orders_app.api.permissions import IsBusinessOrOwnerOrCustomer


class OrdersView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsBusinessOrOwnerOrCustomer]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) |
            Q(business_user=user)
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        response = OrderSerializer(order)
        return Response(response.data, status=status.HTTP_201_CREATED)
