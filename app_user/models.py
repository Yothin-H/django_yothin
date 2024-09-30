from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    address = models.TextField(default='')
    phone = models.CharField(max_length=15,default='')
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    