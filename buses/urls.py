from django.urls import path
from . import views


urlpatterns = [
    path('bus-list/',views.bus_list,name='bus_list'),
    path('add_buss/',views.bus_add,name='add_bus'),
    path('<int:id>/update/',views.bus_update,name='bus_update'),
    path('<int:id>/delete/',views.bus_delete,name='bus_delete'),
    path('routes/',views.route_list,name='route_list'),
    path('add_route/',views.route_add,name='route_add'),
    path('routes/<int:id>/update/',views.route_update,name='route_update'),
    path('routes/<int:id>/delete/',views.route_delete,name='route_delete'),
    path('schedules/',views.sechedule_list,name='schedule_list'),
    path('add_schedule/',views.schedule_add,name='schedule_add'),
    path('seats/',views.seat_list,name='seat_list'),
    path('add_seat/',views.seat_add,name='seat_add'),
    path('search/',views.search_buses,name='search_buses')
]