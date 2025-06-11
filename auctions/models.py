from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=500)
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    img = models.ImageField(upload_to="")
    year = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="won_auctions")
    
    def __str__(self):
        return f"{self.name}  {str(self.amount)}"
    
class Bids(models.Model):
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_list = models.ForeignKey(Listings, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    comment_list = models.ForeignKey(Listings, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} → {self.listing.name}"
