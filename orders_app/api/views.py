from auth_app.models import User
from orders_app.api.permissions import IsBusinessOrOwnerOrCustomer
from orders_app.models import Order
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from orders_app.api.serializers import OrderSerializer, \
    OrderCreateSerializer, OrderDetailSerializer


class OrdersView(ListCreateAPIView):
    """
    View endpoint handling orders listing (GET) and order placements (POST).
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsBusinessOrOwnerOrCustomer]

    def get_queryset(self):
        """
        Filter list to show only records belonging to the requesting
        participant.
        """
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) |
            Q(business_user=user)
        )

    def get_serializer_class(self):
        """
        Dynamically assign serializer classes depending on the execution route.
        """
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Process incoming client transactions and return unified representation
        values.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        response = OrderSerializer(order)
        return Response(response.data, status=status.HTTP_201_CREATED)


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    """
    Detail workspace endpoint serving individual orders management routines.
    """
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = [IsBusinessOrOwnerOrCustomer]
    lookup_url_kwarg = 'order_id'


class OrderCountBusinessUserView(APIView):
    """
    Analytical metric counter tracking a business user's pending/active orders.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Calculate the numerical amount of running agreements."""
        business_user = get_object_or_404(
            User, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user, status='in_progress'
        ).count()
        return Response({'order_count': count})


class CompletedOrderCountBusinessUserView(APIView):
    """
    Analytical metric counter tracking a business user's historically
    archived sales.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Calculate the total amount of successfully completed orders."""
        business_user = get_object_or_404(
            User, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user, status='completed'
        ).count()
        return Response({'completed_order_count': count})
