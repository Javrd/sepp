from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from django.core.validators import ValidationError, EMPTY_VALUES

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user_id>/<filename>
    return 'logos/{0}'.format(filename)

def logos_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user_id>/<filename>
    return 'logos/{0}'.format(filename)

def photos_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user_id>/<filename>
    return 'photos/{0}'.format(filename)

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField('email address', blank=False, unique=True)
    description = models.CharField(max_length=500, null=True)
    logo = models.FileField(null=True, upload_to=logos_directory_path)
    receivers = models.ManyToManyField(
        'self', symmetrical=False, through='Message', related_name="senders")


class Artist(User):
    artistNumber = models.IntegerField(null=True, validators=[MinValueValidator(1)])


class Venue(User):
    geolocation = models.OneToOneField(
        "Geolocation", on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    capacity = models.IntegerField(null=True, validators=[MinValueValidator(1)])


class Photo(models.Model):
    url = models.FileField(upload_to=photos_directory_path)
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
    offeredAmount = models.FloatField(null=True, validators=[MinValueValidator(1.0)])
    date = models.DateTimeField()
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="offers")
    def clean(self):
        if type(self.date) is not datetime:
            raise ValidationError('Fecha invalida.')
        elif self.date < (datetime.today()-timedelta(1)):
            raise ValidationError('La fecha introducida ha pasado.')

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
    def clean(self):
        if type(self.date) is not datetime:
            raise ValidationError('Fecha invalida.')
        elif self.date < (datetime.today()-timedelta(1)):
            raise ValidationError('La fecha introducida ha pasado.')

class Payment(models.Model):
    amount = models.FloatField()
    paypalId = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    performance = models.OneToOneField(Performance, on_delete=models.CASCADE)


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=False)

