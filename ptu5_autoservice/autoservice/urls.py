from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('car/<int:car_id>/', views.car_info, name='car_info'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('my_orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('make_an_order/', views.UserOrderCreateView.as_view(), name='user_order_create'),
]