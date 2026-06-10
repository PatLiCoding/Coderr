from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
#  , RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from orders_app.api.serializers import OrderSerializer, OrderCreateSerializer
from orders_app.models import Order
from orders_app.api.permissions import IsBusinessOrOwnerOrCustomer
from auth_app.models import User


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


class OrderCountBusinessUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(
            User, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user, status='in_progress'
        ).count()
        return Response({'order_count': count})


class CompletedOrderCountBusinessUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(
            User, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user, status='completed'
        ).count()
        return Response({'completed_order_count': count})
