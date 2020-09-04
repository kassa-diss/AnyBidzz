from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime, date, timezone
import math
from math import ceil

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

    def has_expired(self):
        now = datetime.now(timezone.utc)
        expiration = self.Due_date
        if now < expiration:
            return True
        else:
            return False

    def remaining_Time(self):
        
            now = datetime.now(timezone.utc)
            expiration = self.Due_date
            minutes = ceil((expiration - now).total_seconds() / 60)
            
            return int(minutes)
        
            

    



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

    def distance_check(self):  

        #user = UserProfile.objects.filter(user=us_id)
        #lat22 = user.userprofile.latitiude
        #lon22 = user.userprofile.logitude

        R = 6373.0
        lat1 = math.radians(float(self.latitiude))
        lon1 = math.radians(float(self.logitude))
        lat2 = math.radians(52.406374)
        lon2 = math.radians(16.9251681)

        dlon = lon2 - lon1

        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return int(distance)
    
    
    
    
class Bids(models.Model):
    Bid = models.IntegerField(default=0)
    Add_ID =models.TextField(blank=True)
    Title =models.TextField(blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Add_ID)

    def auctionWinner(self):
       highest_bid = Bids.objects.filter(Add_ID=self).order_by('-Bid').first()
       self.winner = highest_bid.user
       return self.winner
    



