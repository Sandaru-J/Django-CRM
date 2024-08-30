from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F

class User(AbstractUser):
    name = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=True,unique=True)
    password = models.CharField(max_length=100, null=False)

    status = models.CharField(max_length=50, null=False)

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

class Product(models.Model):
    stockID = models.IntegerField(null=True) # newly added
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField()

class Order(models.Model): #so here we set as unit base products
    product_ID = models.IntegerField(null=True) # newly added check is this possible to send id from fe
    stockId = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveBigIntegerField()
    useremail = models.EmailField(null=False)

    def save(self, *args, **kwargs):
        # Check if the order is being marked as delivered
        if self.status == 'delivered':
            stock = Stock.objects.get(id=self.stockId)
            stock.quantity = F('quantity') - self.quantity
            stock.save()
        
        super().save(*args, **kwargs)

class Stock(models.Model):
    stock_name = models.CharField(max_length=255)
    supplier_email =models.EmailField(null=False)
    quantity = models.PositiveBigIntegerField()
    status = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_needed = models.DateField(null=True, blank=True)

# report about having proudct id when oreder placed
# i have drf project related to a crm it has fallowing models