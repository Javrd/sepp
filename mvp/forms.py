from django.contrib.auth.forms import *
from django.forms import ModelForm
from .models import Venue, Artist, Geolocation
from django import forms


class VenueForm(UserCreationForm):
    class Meta:
        model = Venue
        fields = ['name', 'email', 'username', 'logo', 'description', 'address', 'capacity']

class GeolocationForm(ModelForm):

    class Meta:
        model = Geolocation
        fields = ['latitude', 'longitude']

'''
class ArtistForm(UserCreationForm):
    class Meta:
        model = Artist
        fields = ['name', 'email', 'username', 'logo', 'description', 'artistNumber']


'''
class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        #exclude = []
        fields = ['name',  'username', 'password', 'email', 'logo', 'artistNumber']


