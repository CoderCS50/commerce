from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryType = models.CharField(max_length=64)
    def __str__(self) -> str:
        return f'{self.categoryType}'



class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='userBid')

    def __str__(self) -> str:
        return str(self.bid)  # Convert the bid value to a string and return it

   
class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name='bidPrice')
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User,null=True, blank=True, related_name="watchlistUser")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    description = models.CharField(max_length=500)
    imgURL = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')

    def __str__(self) -> str:
        return f'{self.title} - Owner: {self.owner}' 
    
class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listing')
    message = models.CharField(max_length=1000)
    def __str__(self) -> str:
        return f' -{self.commenter} on {self.listing.owner}'
    

