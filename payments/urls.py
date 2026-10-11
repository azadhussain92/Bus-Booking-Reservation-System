from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('pay/<str:booking_id>/', views.payment_page, name='payment_page'),
]