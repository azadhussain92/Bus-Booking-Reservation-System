from django.db import models
from booking.models import Booking


PAYMENT_STATUS = [
    ('PENDING','Pending'),
    ('SUCCESS','Success'),
    ('FAILED','Failed')
]

PAYMENT_METHOD = [
    ('UPI','Upi'),
    ('CARD','Card'),
    ('NET_BANKING','Net banking'),
    ('WALLET','Wallet'),
    ('DEMO', 'Demo Payment'),
]
# Create your models here.
class Payment(models.Model):
    booking = models.OneToOneField(Booking,related_name='payments',on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100,unique=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='PENDING')
    paid_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.transaction_id