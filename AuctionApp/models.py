from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime, date, timezone
import math
from math import ceil

# Auction model
class Adds(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    Due_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    bid_total = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.description[:100]

# Add expire function
    def has_expired(self):
        now = datetime.now(timezone.utc)
        expiration = self.Due_date
        if now < expiration:
            return True
        else:
            return False

#calculate auctions' remaining time 
    def remaining_Time(self):
        
            now = datetime.now(timezone.utc)
            expiration = self.Due_date
            minutes = ceil((expiration - now).total_seconds() / 60)
            
            return int(minutes)
        
            

    


#user profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    Self_description = models.CharField(max_length=1000)
    Contact = models.TextField()
    Zipcode = models.IntegerField()
    Address = models.TextField()
    latitiude = models.TextField()
    logitude = models.TextField()
    

    def __str__(self):
        return str(self.user)

    def lat(self):
        lat = float(self.latitiude)

        return float(lat)
    
    def log(self):
        log = float(self.logitude)

        return float(log)


#bid Model 
class Bids(models.Model):
    Bid = models.IntegerField(default=0)
    Add_ID =models.TextField(blank=True)
    Title =models.TextField(blank=True)
    Bid_date = models.DateTimeField(default = datetime.now()) 
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Add_ID)

    def auctionWinner(self):
       highest_bid = Bids.objects.filter(Add_ID=self).order_by('-Bid').first()
       self.winner = highest_bid.user
       return self.winner

    def predict_bid(self):

        pre_adds = Bids.objects.filter(Add_ID=self)
        bid = pre_adds.Bid
        return bid


    



