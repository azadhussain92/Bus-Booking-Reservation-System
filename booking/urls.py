from django.urls import path,include
from . import views


urlpatterns = [
    path('passenger-detail/',views.passenger_details,name='passenger_detail'),
    path('my-booking/',views.my_booking,name='my_booking'),
    path('seat-select/<int:id>/',views.select_seats,name='seat_select'),
    path('setdetails/<int:id>/',views.booking_detail,name='booking_detail'),
    path('all/', views.booking_list, name='booking_list'),
    path('payments/', include('payments.urls')),
    path('passengers/', views.passenger_list, name='passenger_list'),
    path('cancel/<str:booking_id>/',views.cancel_booking,name='cancel_booking'),
]