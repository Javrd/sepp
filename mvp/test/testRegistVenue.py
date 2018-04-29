from django.test import TestCase
from mvp.models import Venue
from mvp.forms import VenueForm


class test_registerVenue(TestCase):
    def setUp(self):
        pass

    def test_RVPositive(self):
        formulario = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertTrue(formulario.is_valid())

    def test_RVNegativeNoEmail(self):
        formulario1 = VenueForm(data={'email': "", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario1.is_valid())

    def test_RVNegativeEmail(self):
        formulario1 = VenueForm(data={'email': "eebsfbdbdsbs", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario1.is_valid())

    def test_RVMissMatchPassword(self):
        formulario2 = VenueForm(data={'email': "testuser@mp.com", 'password1': "test",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario2.is_valid())

    def test_RVNoPassword(self):
        formulario2 = VenueForm(data={'email': "testuser@mp.com", 'password1': "",
                                     'password2': "",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario2.is_valid())

    def test_RVNegativeNoName(self):
        formulario3 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario3.is_valid())

    def test_RVNegativeNoUsername(self):
        formulario4 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario4.is_valid())

    def test_RVNegativeLogo(self):
        formulario5 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "vfsvevg", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario5.is_valid())

    def test_RVNegativeNoLogo(self):
        formulario5 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario5.is_valid())

    def test_RVNegativeDescripcion(self):
        formulario6 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "",
                                     'address': "addresstest", 'capacity': 10})
        self.assertFalse(formulario6.is_valid())

    def test_RVNegativeAddress(self):
        formulario7 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "", 'capacity': 10})
        self.assertFalse(formulario7.is_valid())

    def test_RVNoCapacity(self):
        formulario8 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': None})
        self.assertFalse(formulario8.is_valid())

    def test_RVNegativeCapacity(self):
        formulario8 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': -10})
        self.assertFalse(formulario8.is_valid())

    def test_RVNegativeCeroCapacity(self):
        formulario8 = VenueForm(data={'email': "testuser@mp.com", 'password1': "strongPassuser1",
                                     'password2': "strongPassuser1",
                                     'name': "testuser", 'username': "testusername",
                                     'logo': "www.urlexample.es", 'description': "this is a description",
                                     'address': "addresstest", 'capacity': 0})
        self.assertFalse(formulario8.is_valid())

