from django.db import models
from booking.models import Booking

# Create your models here.
class Ticket(models.Model):
    booking = models.OneToOneField(Booking,related_name='tickets',on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=30,unique=True)
    pdf_file = models.FileField(upload_to='tickets/',blank=True,null=True)
    generated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.ticket_number