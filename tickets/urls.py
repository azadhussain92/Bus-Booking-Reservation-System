from django.urls import path
from . import views


urlpatterns = [
    path('<str:booking_id>/',views.ticket_page,name='ticket_page'),
    path('<str:booking_id>/download/',views.download_ticket,name='download_ticket'),
]