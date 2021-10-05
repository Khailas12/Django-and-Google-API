from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    address = models.CharField(verbose_name='Address', max_length=120, null=True, blank=False)
    town = models.CharField(verbose_name='Town/City', max_length=50, null=True, blank=False)
    country = models.CharField(verbose_name='Country', max_length=30, null=True, blank=False)
    
    longitude = models.CharField(verbose_name='Longitude', max_length=50, null=True, blank=False)
    latitude = models.CharField(verbose_name='Latitude', max_length=50, null=True, blank=False)
    
    captcha_score = models.FloatField(default=0.0)  # this will authorize to the score submission verification connecting with the recaptcha API, highest is 1.0 and default is 0.0
    
    has_profile = models.BooleanField(default=False)    # when a user signs up and fills eveything then it'll be True
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return f'{self.user}'