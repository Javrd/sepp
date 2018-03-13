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
from mvp.models import Media
from mvp.models import Offer
from mvp.models import Performance
from mvp.models import Payment


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
            timeStamp = datetime.datetime.strptime(line[0], '%Y-%m-%d %I:%M%p')
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


def importMedias():
    """Import Medias from medias.csv to database."""
    with open('mvp/data/medias.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            url = line[0]
            artisId = Artist.objects.get(pk=line[1])
            mediaId = line[2]
            print(line)
            new = Media.objects.create(url=url, artist=artisId, id=mediaId)

            new.save()


def importOffers():
    """Import Offers from offers.csv to database."""
    with open('mvp/data/offers.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            name = line[0]
            description = line[1]
            offeredAmount = line[2]
            date = datetime.datetime.strptime(line[3], '%Y-%m-%d')
            venue = Venue.objects.get(pk=line[4])
            offerId = line[5]
            print(line)
            new = Offer.objects.create(name=name, description=description,
                                       offeredAmount=offeredAmount, date=date,
                                       venue=venue, id=offerId)

            new.save()


def importPerfomances():
    """Import performances from performances.csv to database."""
    with open('mvp/data/performances.csv') as csvfile:
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
            print(line)
            new = Performance.objects.create(name=name,
                                             description=description,
                                             date=date, public=public,
                                             artist=artist, venue=venue,
                                             id=performanceId)

            new.save()


def importPayments():
    """Import Payment from payment.csv to database."""
    with open('mvp/data/payments.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(spamreader.__next__())
        for line in spamreader:
            amount = line[0]
            date = datetime.datetime.strptime(line[1], '%Y-%m-%d')
            user = User.objects.get(pk=line[2])
            performance = Performance.objects.get(pk=line[3])
            paymentId = line[4]
            print(line)
            new = Payment.objects.create(amount=amount,
                                         date=date, user=user,
                                         performance=performance,
                                         id=paymentId)

            new.save()


"""Delete all data from database"""
Account.objects.all().delete()
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
importArtists()
importVenues()
importMessages()
importPhotos()
importTags()
importMedias()
importOffers()
importPerfomances()
importPayments()
