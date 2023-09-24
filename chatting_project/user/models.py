from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    
class VerifyToken(models.Model):
    otp = models.IntegerField()
    created_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    

class ForgetPasswordToken(models.Model):
    token = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    