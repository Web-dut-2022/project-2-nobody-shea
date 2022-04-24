from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionsListings(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=15)
    image = models.ImageField(null=True,blank=True)
    imgURL = models.URLField(blank= True);   
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=64,default="Other")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class BidRecord(models.Model):
    aid = models.ForeignKey(AuctionsListings, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Comments(models.Model):
    aid = models.ForeignKey(AuctionsListings, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Watchlist(models.Model):
    aid = models.ForeignKey(AuctionsListings, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)