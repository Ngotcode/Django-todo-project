from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)       #this is un-editable but need to see it in the Admin database, seee admin.py
    datecompleted = models.DateTimeField(null=True, blank=True)      #date/time units designated null as compare to blank
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #need this to distinguish between different users' todos app


#name model objects 
    def __str__(self):
        return self.title