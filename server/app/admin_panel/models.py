from django.db import models

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)

class Agent(models.Model):
    name = models.CharField(max_length=100)
    machine = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    statut = models.BooleanField(default=False)