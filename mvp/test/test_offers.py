from django.test import TestCase
from mvp.forms import OfferForm
from mvp.models import Venue

class test_Offers(TestCase):
    def setUp(self):
        pass

    def test_OfferPositive(self):
        formulario = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': 10.0, 'date': "10/3/2019"})
        self.assertTrue(formulario.is_valid())

    def test_OfferNegativeNoName(self):
        formulario1 = OfferForm(user= None,data={'name': "", 'description': "this is a description",
                                     'offeredAmount': 10.0, 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNoneName(self):
        formulario1 = OfferForm(user= None,data={'name': None, 'description': "this is a description",
                                     'offeredAmount': 10.0, 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNoDesc(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "",
                                     'offeredAmount': 10.0, 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNoneDesc(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': None,
                                     'offeredAmount': 10.0, 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNoAmount(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': 0.0, 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeInvalidAmount(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': "hola", 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNoneAmount(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': None, 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNoDate(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': 10.0, 'date': ""})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeInvalidDate(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': 10.0, 'date': "ivewvoinewve"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativePastDate(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': 10.0, 'date': "10/3/2017"})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNoneDate(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': 10.0, 'date': None})
        self.assertFalse(formulario1.is_valid())

    def test_OfferNegativeNegtiveAmount(self):
        formulario1 = OfferForm(user= None,data={'name': "testOfferName", 'description': "this is a description",
                                     'offeredAmount': -10.0, 'date': "10/3/2019"})
        self.assertFalse(formulario1.is_valid())

