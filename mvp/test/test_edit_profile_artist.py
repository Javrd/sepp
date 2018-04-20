from django.test import TestCase
from mvp.models import Artist
from mvp.forms import ArtistProfileForm, PhotoForm, TagForm, MediaForm


class test_edit_profile_artist(TestCase):
    def setUp(self):
        self.register = {
            'username': 'testusername',
            'password': 'testpass55',
            'email': 'testemail@email.com',
            'name': "name",
            'logo': "https://www.logotest1.com",
            'description': "description_test1",
            'artistNumber': 5,
        }

    def test_positive1(self):

        form = ArtistProfileForm(data={'email': "artist_test1@email.com",
                                     'name': "name",
                                     'logo': "https://www.logotest1.com",
                                     'description': "description_test1",
                                     'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertTrue(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())


    #Invalid Email
    def test_negative1(self):

        form = ArtistProfileForm(data={'email': "artist_test1",
                                     'name': "name",
                                     'logo': "https://www.logotest1.com",
                                     'description': "description_test1",
                                     'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())

    #Invalid name
    def test_negative2(self):

        form = ArtistProfileForm(data={'email': "artist_test1@emai.com",
                                     'name': "",
                                     'logo': "https://www.logotest1.com",
                                     'description': "description_test1",
                                     'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())

    #Invalid logo
    def test_negative3(self):

        form = ArtistProfileForm(data={'email': "artist_test1@email.com",
                                     'name': "name",
                                     'logo': "logo",
                                     'description': "description_test1",
                                     'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())

    #Invalid description
    def test_negative4(self):

        form = ArtistProfileForm(data={'email': "artist_test1",
                                     'name': "name",
                                     'logo': "https://www.logotest1.com",
                                     'description': "",
                                     'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())


    #Invalid artistNumber
    def test_negative5(self):

        form = ArtistProfileForm(data={'email': "artist_test1@email.com",
                                     'name': "name",
                                     'logo': "https://www.logotest1.com",
                                     'description': "description_test1",
                                     'artistNumber': None})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertFalse(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())

    #Invalid Photo1
    def test_negative6(self):

        form = ArtistProfileForm(data={'email': "artist_test1@email.com",
                                     'name': "name",
                                     'logo': "https://www.logotest1.com",
                                     'description': "description_test1",
                                     'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "photo", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertTrue(form.is_valid())
        self.assertFalse(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())


    #Invalid Tag1
    def test_negative7(self):

        form = ArtistProfileForm(data={'email': "artist_test1@email.com",
                                     'name': "name",
                                     'logo': "https://www.logotest1.com",
                                     'description': "description_test1",
                                     'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': None, 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertTrue(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertFalse(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertTrue(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())


    #Invalid Media1
    def test_negative8(self):
        form = ArtistProfileForm(data={'email': "artist_test1@email.com",
                                           'name': "name",
                                           'logo': "https://www.logotest1.com",
                                           'description': "description_test1",
                                           'artistNumber': 5})
        user = Artist.objects.create_user(**self.register)

        formPhoto1 = PhotoForm(data={'url': "https://www.photo.com", 'id': user.id})
        formPhoto2 = PhotoForm(data={'url': "https://www.photo2.com", 'id': user.id})

        formTag1 = TagForm(data={'name': "nameTag1", 'id': user.id})
        formTag2 = TagForm(data={'name': "nameTag2", 'id': user.id})

        formMedia1 = MediaForm(data={'url': "youtube", 'id': user.id})
        formMedia2 = MediaForm(data={'url': "https://www.youtube.com", 'id': user.id})

        self.assertTrue(form.is_valid())
        self.assertTrue(formPhoto1.is_valid())
        self.assertTrue(formPhoto2.is_valid())
        self.assertTrue(formTag1.is_valid())
        self.assertTrue(formTag2.is_valid())
        self.assertFalse(formMedia1.is_valid())
        self.assertTrue(formMedia2.is_valid())