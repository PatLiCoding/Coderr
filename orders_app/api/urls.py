from django.urls import path
from .views import OrdersView, \
    OrderCountBusinessUserView, CompletedOrderCountBusinessUserView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
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
