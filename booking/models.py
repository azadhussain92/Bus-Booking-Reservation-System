from django.db import models
from django.contrib.auth.models import User
from buses.models import BusSchedule,BusSeat


STATUS_CHOISE = [
    ('CONFIRMED','Confirmed'),
    ('PENDING','Pending'),
    ('CANCELLED','Cancelled'),
]

# Create your models here.
#booking models 
class Booking(models.Model):
    user = models.ForeignKey(User,related_name='bookings',on_delete=models.CASCADE)
    schedule = models.ForeignKey(BusSchedule,related_name='bookings',on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=30,unique=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOISE,default='PENDING')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking_id


#passenger models

GENDER_CHOISE =[
    ('MALE','Male'),
    ('FEMALE','Female'),
    ('OTHER','Other')
]

class Passenger(models.Model):
    booking = models.ForeignKey(Booking,related_name='passengers',on_delete=models.CASCADE)
    seat = models.ForeignKey(BusSeat,related_name='passengers',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender =models.CharField(max_length=20,choices=GENDER_CHOISE)
    phone = models.CharField(max_length=17)


    def __str__(self):
        return self.name