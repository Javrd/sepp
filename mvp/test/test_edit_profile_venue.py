from django.test import TestCase
from mvp.models import Venue
from mvp.forms import VenueProfileForm, PhotoForm, TagForm, MediaForm


class test_edit_profile_artist(TestCase):
    def setUp(self):
        self.register = {
            'email': "testuser@mp.com",
            'password': "strongPassuser1",
            'name': "testuser",
            'username': "testusername",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10
        }

    def test_positive1(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "testuser",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertTrue(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid email
    def test_negative2(self):

        form = VenueProfileForm(data={'email': "testuser",
            'name': "testuser",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid name
    def test_negative3(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid logo
    def test_negative4(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "testuser",
            'logo': "urlexample",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid description
    def test_negative5(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "testuser",
            'logo': "www.urlexample.es",
            'description': None,
            'address': "addresstest",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid address
    def test_negative6(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "testuser",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid capacity
    def test_negative7(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "testuser",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': None})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid photo1
    def test_negative8(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "testuser",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': None, 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        self.assertTrue(form.is_valid())
        self.assertFalse(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())


    #Invalid photo2
    def test_negative9(self):

        form = VenueProfileForm(data={'email': "testuser@email.com",
            'name': "testuser",
            'logo': "www.urlexample.es",
            'description': "this is a description",
            'address': "addresstest",
            'capacity': 10})

        user = Venue.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo1.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "photo2", 'id': user.id})

        self.assertTrue(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertFalse(formPhoto2.is_valid())