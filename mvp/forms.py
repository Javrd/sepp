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
		
class ArtistForm(forms.Form):
    name = forms.CharField(max_length=30, help_text='Required.')
    username = forms.CharField(max_length=30, help_text='Required.')
    password = forms.CharField(max_length=30, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    description = forms.CharField(max_length=500,required=False)
    logo = forms.URLField(required=False)
    artistNumber = forms.IntegerField(required=False)
    class Meta:
        model = Artist
        fields = ['name',  'username', 'password', 'email', 'logo', 'artistNumber']
