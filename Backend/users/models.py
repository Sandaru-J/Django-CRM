from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True,unique=True)
    password = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    contact_number = models.CharField(max_length=20, null=True)
    type_of_business = models.CharField(max_length=100, null=True)
    delivery_address = models.TextField(null=True)
    company_name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    supply_capacity = models.IntegerField(null=True)

    username = None

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

# Create your models here.
