from django.db import models
from datetime import datetime
from user.models import User



    
    
class Room(models.Model):
    user1 = models.CharField(max_length=150)
    user2 = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.user1} | {self.user2}"
    
    
class Chat(models.Model):
    message = models.TextField()
    send_date = models.DateTimeField(default = datetime.now)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    msg_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_msg_from')
    msg_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_to")
    def __str__(self):
        return f"from {self.msg_from.username} to {self.msg_to.username}"