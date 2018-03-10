from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Account(AbstractUser):
    pass

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    description = models.CharField(max_length=500)
    logo = models.URLField()
    sentMessage = models.ManyToManyField('self', symmetrical=False, through='Message')
    account = models.OneToOneField(Account, on_delete=models.CASCADE)


class Artist(User):
    artistNumber = models.IntegerField()


class Venue(User):
    geolocation = models.OneToOneField("Geolocation", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    capactity = models.IntegerField()


class Photo(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Media(models.Model):
    url = models.URLField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Geolocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Message(models.Model):
    timeStamp = models.DateTimeField()
    text = models.CharField(max_length=500)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)


class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    offeredAmount = models.FloatField()
    date = models.DateTimeField()


class Performance(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateTimeField()
    paymentAmount = models.FloatField()
    paymentDate = models.DateTimeField()
    public = models.BooleanField()