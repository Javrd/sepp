# -*- coding: utf-8 -*-
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
from mvp.models import Geolocation
from mvp.models import Message
from mvp.models import Photo
from mvp.models import Tag
from mvp.models import Media
from mvp.models import Offer
from mvp.models import Performance
from mvp.models import Payment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


def createPermissions():
    ct = ContentType.objects.get(app_label='mvp', model='user')
    new = Permission.objects.create(codename='artist', name='Can View Artist', content_type=ct)
    new.save()
    new = Permission.objects.create(codename='venue', name='Can View Venue', content_type=ct)
    new.save()


def importArtists():
    """Import artist from artists.csv to database."""
    permission = Permission.objects.get(codename='artist')
    with open('mvp/data/artists.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:

            nombre = line[0]
            email = line[1]
            description = line[2]
            logo = line[3]
            integrantes = line[4]
            artisId = line[5]
            username = line[6]

            new = Artist.objects.create(username=username, email=email,
                                        name=nombre, description=description,
                                        logo=logo, artistNumber=integrantes,
                                        id=artisId)
            new.set_password(username)
            new.user_permissions.add(permission)
            new.save()


def importVenues():
    """Import venues from venues.csv to database."""
    permission = Permission.objects.get(codename='venue')
    with open('mvp/data/venues.csv', encoding='utf-8') as csvfile:
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
            username = line[8]
            geo = geo.split('/')
            geos = Geolocation.objects.create(
                latitude=float(geo[0]), longitude=float(geo[1]))
            new = Venue.objects.create(username=username, email=email,
                                       name=nombre, description=description,
                                       logo=logo, geolocation=geos,
                                       address=address, capacity=capacity,
                                       id=venueId)
            new.set_password(username)
            new.user_permissions.add(permission)
            new.save()


def importMessages():
    """Import messages from messages.csv to database."""
    with open('mvp/data/messages.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            timeStamp = datetime.datetime.strptime(line[0], '%Y-%m-%d %I:%M%p')
            text = line[1]
            sender = User.objects.get(pk=line[2])
            receiver = User.objects.get(pk=line[3])
            messageId = line[4]

            new = Message.objects.create(timeStamp=timeStamp, text=text,
                                         sender=sender, receiver=receiver,
                                         id=messageId)

            new.save()


def importPhotos():
    """Import photos from photos.csv to database."""
    with open('mvp/data/photos.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            photoUrl = line[0]
            userId = User.objects.get(pk=line[1])
            photoId = line[2]
            new = Photo.objects.create(url=photoUrl, user=userId, id=photoId)

            new.save()


def importTags():
    """Import tags from tags.csv to database."""
    with open('mvp/data/tags.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            name = line[0]
            artisId = Artist.objects.get(pk=line[1])
            tagId = line[2]
            new = Tag.objects.create(name=name, artist=artisId, id=tagId)

            new.save()


def importMedias():
    """Import Medias from medias.csv to database."""
    with open('mvp/data/medias.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            url = line[0]
            artisId = Artist.objects.get(pk=line[1])
            mediaId = line[2]
            new = Media.objects.create(url=url, artist=artisId, id=mediaId)

            new.save()


def importOffers():
    """Import Offers from offers.csv to database."""
    with open('mvp/data/offers.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            name = line[0]
            description = line[1]
            offeredAmount = line[2]
            date = datetime.datetime.strptime(line[3], '%Y-%m-%d')
            venue = Venue.objects.get(pk=line[4])
            offerId = line[5]
            new = Offer.objects.create(name=name, description=description,
                                       offeredAmount=offeredAmount, date=date,
                                       venue=venue, id=offerId)

            new.save()


def importPerfomances():
    """Import performances from performances.csv to database."""
    with open('mvp/data/performances.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            name = line[0]
            description = line[1]
            date = datetime.datetime.strptime(line[2], '%Y-%m-%d')
            public = line[3]
            artist = Artist.objects.get(pk=line[4])
            venue = Venue.objects.get(pk=line[5])
            performanceId = line[6]
            new = Performance.objects.create(name=name,
                                             description=description,
                                             date=date, public=public,
                                             artist=artist, venue=venue,
                                             id=performanceId)

            new.save()


def importPayments():
    """Import Payment from payment.csv to database."""
    with open('mvp/data/payments.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            amount = line[0]
            date = datetime.datetime.strptime(line[1], '%Y-%m-%d')
            user = User.objects.get(pk=line[2])
            performance = Performance.objects.get(pk=line[3])
            paymentId = line[4]
            new = Payment.objects.create(amount=amount,
                                         date=date, user=user,
                                         performance=performance,
                                         id=paymentId)

            new.save()


"""Delete all data from database"""
Geolocation.objects.all().delete()
Permission.objects.all().delete()
Artist.objects.all().delete()
Venue.objects.all().delete()
Message.objects.all().delete()
Photo.objects.all().delete()
Tag.objects.all().delete()
Media.objects.all().delete()
Offer.objects.all().delete()
Performance.objects.all().delete()
Payment.objects.all().delete()


"""Import new data"""
createPermissions()
importArtists()
importVenues()
importMessages()
importPhotos()
importTags()
importMedias()
importOffers()
importPerfomances()
importPayments()