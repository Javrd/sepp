from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField('email address', blank=False, unique=True)
    description = models.CharField(max_length=500, null=True)
    logo = models.URLField(null=True)
    receivers = models.ManyToManyField(
        'self', symmetrical=False, through='Message', related_name="senders")


class Artist(User):
    artistNumber = models.IntegerField(null=True)


class Venue(User):
    geolocation = models.OneToOneField(
        "Geolocation", on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    capacity = models.IntegerField(null=True)


class Photo(models.Model):
    url = models.URLField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="photos")


class Tag(models.Model):
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="tags")


class Media(models.Model):
    url = models.URLField()
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="media")


class Geolocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


# Message system
class Message(models.Model):
    timeStamp = models.DateTimeField()
    text = models.CharField(max_length=500)
    sender = models.ForeignKey(
        User, related_name='sentMessages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='receivedMessages', on_delete=models.CASCADE)


# Offers from venues
class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    offeredAmount = models.FloatField(null=True)
    date = models.DateTimeField()
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="offers")


# Announcements
class Performance(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateTimeField()
    public = models.BooleanField()
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="performances")
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="performances")


class Payment(models.Model):
    amount = models.FloatField()
    paypalId = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    performance = models.OneToOneField(Performance, on_delete=models.CASCADE)


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=False)

