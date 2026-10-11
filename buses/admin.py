from django.contrib import admin
from buses.models import Buses,BusRoute,BusSchedule,BusSeat

# Register your models here.
admin.site.register(Buses)
admin.site.register(BusRoute)
admin.site.register(BusSchedule)
admin.site.register(BusSeat)