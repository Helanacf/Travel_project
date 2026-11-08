from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Register(AbstractUser):
    phone=models.CharField(max_length=10,null=True, blank=True)
    role=models.CharField(max_length=10,default="Admin")
    profile=models.ImageField(upload_to='profile/',null=True, blank=True)


class Places(models.Model):
    name = models.CharField(max_length=20,null=True,blank=True)
    location = models.CharField(max_length=50,null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='tourist_places/', null=True, blank=True)
    category = models.CharField(max_length=100, choices=[
        ('hill', 'Hill Station'),
        ('beach', 'Beach'),
        ('heritage', 'Heritage Site'),
        ('adventure', 'Adventure Spot'),
        ('religious', 'Religious Place'),
        ('wildlife', 'Wildlife Sanctuary'),
        ('others', 'Others'),
    ])
    entry_fee = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    best_season = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
