from django.db import models
from django.contrib.auth.models import User




ROLE_CHOISES = [
    ('ADMIN','Admin'),
    ('CUSTOMER','Customer'),
    ('BUS_OPERATOR','Bus operator')
]
# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    phone = models.CharField(max_length=17)
    role = models.CharField(max_length=20,choices=ROLE_CHOISES,default='CUSTOMER')
    profile_image = models.ImageField(upload_to='profile/',blank= True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username