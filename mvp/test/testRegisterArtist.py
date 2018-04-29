from django.test import TestCase
from mvp.models import Artist
from mvp.forms import ArtistForm


class test_register_artist(TestCase):
    def setUp(self):
       pass

    def test_positiveRA1(self):
        form1 = ArtistForm(data={'email': "artist_test1@test.com", 'password1': "password_test1",
                                 'password2': "password_test1", 'name': "name_test1", 'username': "username_test1",
                                    'logo': "https://www.logotest1.com", 'description': "description_test1",
                                    'artistNumber': 5})
        self.assertTrue(form1.is_valid())

    def test_positiveRA2(self):
        form2 = ArtistForm(data={'email': "artist_test2@test.com", 'password1': "password_test2", 'password2': "password_test2",
                                     'name': "name_test2", 'username': "username_test2",
                                     'logo': "https://www.logotest2.com", 'description': "description_test2",
                                     'artistNumber': 5})
        self.assertTrue(form2.is_valid())

    def test_positiveRA3(self):
        form3 = ArtistForm(data={'email': "artist_test3@test.com", 'password1': "password_test3", 'password2': "password_test3",
                                     'name': "name_test3", 'username': "username_test3",
                                     'logo': "https://www.logotest3.com", 'description': "description_test3",
                                     'artistNumber': 1})
        self.assertTrue(form3.is_valid())

    def test_negativeRAnoEmail(self):
        form4 = ArtistForm(data={'email': "", 'password1': "password_test1", 'password2': "password_test1",
                                     'name': "name_test1", 'username': "username_test1",
                                     'logo': "https://www.logotest1.com", 'description': "description_test1",
                                     'artistNumber': 10})
        self.assertFalse(form4.is_valid())

    def test_negativeRAbadEmail(self):
        form4 = ArtistForm(data={'email': "vwvesfd", 'password1': "password_test1", 'password2': "password_test1",
                                     'name': "name_test1", 'username': "username_test1",
                                     'logo': "https://www.logotest1.com", 'description': "description_test1",
                                     'artistNumber': 10})
        self.assertFalse(form4.is_valid())

    def test_negativeRAnoPassword(self):
        form5 = ArtistForm(data={'email': "artist_test2@test.com", 'password1': "", 'password2': "",
                                     'name': "name_test2", 'username': "username_test2",
                                     'logo': "https://www.logotest2.com", 'description': "description_test2",
                                     'artistNumber': 3})
        self.assertFalse(form5.is_valid())

    def test_negativeRAnoName(self):
        form6 = ArtistForm(data={'email': "artist_test3@test.com", 'password1': "password_test3", 'password2': "password_test3",
                                     'name': "", 'username': "username_test3",
                                     'logo': "https://www.logotest3.com", 'description': "description_test3",
                                     'artistNumber': 5})
        self.assertFalse(form6.is_valid())

    def test_negativeRAnoUserName(self):
        form7 = ArtistForm(data={'email': "artist_test4@test.com", 'password1': "password_test4", 'password2': "password_test4",
                                     'name': "name_test4", 'username': "",
                                     'logo': "https://www.logotest4.com", 'description': "description_test4",
                                     'artistNumber': 8})
        self.assertFalse(form7.is_valid())

    def test_negativeRAmissMatchPasswords(self):
        form8 = ArtistForm(data={'email': "artist_test4@test.com", 'password1': "password_test45", 'password2': "password_test4",
                                     'name': "name_test4", 'username': "username_test5",
                                     'logo': "https://www.logotest4.com", 'description': "description_test4",
                                     'artistNumber': 8})
        self.assertFalse(form8.is_valid())

    def test_negativeRACeroArtist(self):
        form1 = ArtistForm(data={'email': "artist_test1@test.com", 'password1': "password_test1",
                                 'password2': "password_test1", 'name': "name_test1", 'username': "username_test1",
                                    'logo': "https://www.logotest1.com", 'description': "description_test1",
                                    'artistNumber': 0})
        self.assertFalse(form1.is_valid())

    def test_RAnegativeArtist(self):
        form1 = ArtistForm(data={'email': "artist_test1@test.com", 'password1': "password_test1",
                                 'password2': "password_test1", 'name': "name_test1", 'username': "username_test1",
                                    'logo': "https://www.logotest1.com", 'description': "description_test1",
                                    'artistNumber': -8})
        self.assertFalse(form1.is_valid())

    def test_positiveRANoLogo(self):
        form1 = ArtistForm(data={'email': "artist_test1@test.com", 'password1': "password_test1",
                                 'password2': "password_test1", 'name': "name_test1", 'username': "username_test1",
                                    'logo': "", 'description': "description_test1",
                                    'artistNumber': 5})
        self.assertFalse(form1.is_valid())

    def test_positiveRABadLogo(self):
        form1 = ArtistForm(data={'email': "artist_test1@test.com", 'password1': "password_test1",
                                 'password2': "password_test1", 'name': "name_test1", 'username': "username_test1",
                                    'logo': "evevevs", 'description': "description_test1",
                                    'artistNumber': 5})
        self.assertFalse(form1.is_valid())





