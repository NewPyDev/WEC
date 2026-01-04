from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('history/', views.order_history, name='order_history'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/update-status/', views.order_update_status, name='order_update_status'),
    path('<int:pk>/shipping-label/', views.order_shipping_label, name='order_shipping_label'),
]
