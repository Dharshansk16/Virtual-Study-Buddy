from django.db import models
from django.contrib.auth.models import  User #Importing Usermodel

# Create your models here.
# Creates table by using the class data

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #On deleting the topic the room associated with it don't get deleted from the database
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank = True)#null=True means user  can keep this field empty
                                                            #blank = True means when the form is submit the form can be empty and can be updated later.
    # participants =
    updated = models.DateTimeField(auto_now=True) # Takes time stamp every time a user submits or saves.
    created = models.DateTimeField(auto_now_add=True) #  Takes time stamp when we first submit or save(created time).

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE) #Where User is a class Imported from django.contrib line 2
    room =models.ForeignKey(Room, on_delete=models.CASCADE) #One to Many relation i.e one user can have multiple rooms.
    #When a user deletes a room all the messages in the room gets deleted from the database using models.CASCADE.
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
    