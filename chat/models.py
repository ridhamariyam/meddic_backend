from django.db import models
from medcoapp.models import account


    
class DirectMessage(models.Model): 

    sender = models.ForeignKey(account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(account, on_delete=models.CASCADE, related_name='reciever')

    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    send_at = models.DateTimeField(auto_now_add=True)
    thread_name=models.CharField(null=True,blank=True,max_length=200)
    class Meta:
        ordering = ['send_at']
        

    def __str__(self):
        return f"{self.sender} - {self.receiver}"