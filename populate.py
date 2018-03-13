"""Import models from mvp/data/xxx.csv."""
import csv
import datetime
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'artinbar.settings'
django.setup()
from mvp.models import Artist
from mvp.models import Venue
from mvp.models import User
from mvp.models import Account
from mvp.models import Geolocation
from mvp.models import Message
from mvp.models import Photo
from mvp.models import Tag


def importArtists():
    """Import artist from artists.csv to database."""
    with open('mvp/data/artists.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:

            nombre = line[0]
            email = line[1]
            description = line[2]
            logo = line[3]
            integrantes = line[4]
            artisId = line[5]
            print(line)

            acc = Account.objects.create_user(nombre, email, nombre)
            new = Artist.objects.create(name=nombre, description=description,
                                        logo=logo, artistNumber=integrantes,
                                        account=acc, id=artisId)
            new.save()


def importVenues():
    """Import venues from venues.csv to database."""
    with open('mvp/data/venues.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:

            nombre = line[0]
            email = line[1]
            description = line[2]
            logo = line[3]
            geo = line[4]
            address = line[5]
            capacity = line[6]
            venueId = line[7]
            print(line)
            geo = geo.split('/')
            acc = Account.objects.create_user(nombre, email, nombre)
            geos = Geolocation.objects.create(
                latitude=float(geo[0]), longitude=float(geo[1]))
            new = Venue.objects.create(name=nombre, description=description,
                                       logo=logo, geolocation=geos,
                                       address=address, capacity=capacity,
                                       account=acc, id=venueId)

            new.save()


def importMessages():
    """Import messages from messages.csv to database."""
    with open('mvp/data/messages.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            timeStamp = datetime.datetime.now()
            text = line[1]
            sender = User.objects.get(pk=line[2])
            receiver = User.objects.get(pk=line[3])
            messageId = line[4]
            print(line)

            new = Message.objects.create(timeStamp=timeStamp, text=text,
                                         sender=sender, receiver=receiver,
                                         id=messageId)

            new.save()


def importPhotos():
    """Import photos from photos.csv to database."""
    with open('mvp/data/photos.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            photoUrl = line[0]
            userId = User.objects.get(pk=line[1])
            photoId = line[2]
            print(line)
            new = Photo.objects.create(url=photoUrl, user=userId, id=photoId)

            new.save()


def importTags():
    """Import tags from tags.csv to database."""
    with open('mvp/data/tags.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            name = line[0]
            artisId = Artist.objects.get(pk=line[1])
            tagId = line[2]
            print(line)
            new = Tag.objects.create(name=name, artist=artisId, id=tagId)

            new.save()


"""Delete all data from database"""
Account.objects.all().delete()
Artist.objects.all().delete()
Venue.objects.all().delete()
Message.objects.all().delete()
Photo.objects.all().delete()
Tag.objects.all().delete()
"""Import new data"""
importArtists()
importVenues()
importMessages()
importPhotos()
importTags()
