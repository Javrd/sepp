from django.test import TestCase
from mvp.models import Artist,Venue,Performance
from mvp.forms import PerformanceForm

class test_Performance(TestCase):
    def setUp(self):
        self.registerArtist = {
            'username': 'artitssername',
            'password': 'testpass55',
            'email': 'testemail@email.com',
            'name': "name",
            'logo': "https://www.logotest1.com",
            'description': "description_test1",
            'artistNumber': 5,
        }
        self.registerVenue = {
            'email': "testuser@mp.com",
            'password': "strongPassuser1",
            'name': "testuser",
            'username': "venuesername",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10
        }


    def test_PerformancePositive(self):
        venue = Venue.objects.create_user(**self.registerVenue)
        artist = Artist.objects.create_user(**self.registerArtist)
        performance = PerformanceForm(data={'name': "testperformance", 'description': "testing performance", 'date': "2019-04-24",
                                            'public': True, 'venue': venue, 'artist': artist})
        self.assertTrue(performance.is_valid())

    def test_PerformancePastDate(self):
        venue = Venue.objects.create_user(**self.registerVenue)
        artist = Artist.objects.create_user(**self.registerArtist)
        performance = PerformanceForm(data={'name': "testperformance", 'description': "testing performance", 'date': "2017-04-24",
                                            'public': True, 'venue': venue, 'artist': artist})
        self.assertFalse(performance.is_valid())

    def test_PerformanceInvalidDate(self):
        venue = Venue.objects.create_user(**self.registerVenue)
        artist = Artist.objects.create_user(**self.registerArtist)
        performance = PerformanceForm(data={'name': "testperformance", 'description': "testing performance", 'date': "evgw",
                                            'public': True, 'venue': venue, 'artist': artist})
        self.assertFalse(performance.is_valid())

    def test_PerformanceNoName(self):
        venue = Venue.objects.create_user(**self.registerVenue)
        artist = Artist.objects.create_user(**self.registerArtist)
        performance = PerformanceForm(data={'name': "", 'description': "testing performance", 'date': "2019-04-24",
                                            'public': True, 'venue': venue, 'artist': artist})
        self.assertFalse(performance.is_valid())

    def test_PerformanceNoDescription(self):
        venue = Venue.objects.create_user(**self.registerVenue)
        artist = Artist.objects.create_user(**self.registerArtist)
        performance = PerformanceForm(data={'name': "testperformance", 'description': "", 'date': "2019-04-24",
                                            'public': True, 'venue': venue, 'artist': artist})
        self.assertFalse(performance.is_valid())