from django.urls import path
from .views import OrdersView, OrderDetailView, \
    OrderCountBusinessUserView, CompletedOrderCountBusinessUserView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
    path(
        'orders/<int:order_id>/',
        OrderDetailView.as_view(),
        name='orders-detail'),
    path(
        'order-count/<int:business_user_id>/',
        OrderCountBusinessUserView.as_view(),
        name='order-count'
    ),

    path(
        'completed-order-count/<int:business_user_id>/',
        CompletedOrderCountBusinessUserView.as_view(),
        name='completed-order-count'
    ),
]
