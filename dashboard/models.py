from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    image = models.ImageField(upload_to="media/", default="media/logo.png", null=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    def __str__(self):
        return self.user.username

class Auction(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    startprice = models.IntegerField(default=1)
    image = models.ImageField(upload_to="auction/")
    statusvalue = (("Soon", "Soon"), ("Live", "Live"), ("Expired", "Expired"))
    status = models.CharField(max_length=10, default="Soon", choices=statusvalue)
    time = models.IntegerField(default=1)
    timestart = models.DateTimeField(null=True, blank=True)
    timeend = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', null=True, blank=True)
    def __str__(self):
        return self.title

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    auction_balance = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user_id} {self.auction_id} {self.auction_balance}"