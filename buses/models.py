from django.db import models
from django.contrib.auth.models import User


BUS_TYPE_CHOISE = [
    ('AC', 'AC'),
    ('NON_AC', 'Non AC'),
    ('SLEEPER', 'Sleeper'),
    ('SEATER', 'Seater'),
    ('AC_SLEEPER', 'AC Sleeper'),
]

# Create your models here.
class Buses(models.Model):
    operator = models.ForeignKey(User,related_name='buses',on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=20,unique=True)
    bus_name = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=20,choices=BUS_TYPE_CHOISE)
    total_seats = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.bus_name} - {self.bus_number}"

#route models
class BusRoute(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.PositiveIntegerField(help_text="Distancein KM")
    duration = models.DurationField(null=True,blank=True)

    def __str__(self):
        return f"{self.source} - {self.distance}"


#bus schedule models
class BusSchedule(models.Model):
    bus = models.ForeignKey(Buses,related_name='schedule',on_delete=models.CASCADE)
    route = models.ForeignKey(BusRoute,related_name='schedule',on_delete=models.CASCADE)
    journey_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    boarding_point = models.CharField(max_length=200)
    dropping_point = models.CharField(max_length=200)
    is_daily = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bus.bus_name} - {self.route.source} to {self.route.destination} - {self.journey_date}"


SEAT_TYPE_CHOISE = [
    ('SEATER','Seater'),
    ('SLEEPER','Sleeper')
]
#seating models
class BusSeat(models.Model):
    bus = models.ForeignKey(Buses,related_name='seats',on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20,choices=SEAT_TYPE_CHOISE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('bus','seat_number')

    def __str__(self):
        return f"{self.bus.bus_number} - {self.seat_number}"
