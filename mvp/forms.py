from django.forms import ModelForm
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import *

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'description', 'offeredAmount', 'date']

    def __init__(self, user, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.venue = user

class GeolocationForm(ModelForm):

    class Meta:
        model = Geolocation
        fields = ['latitude', 'longitude']


class VenueForm(UserCreationForm):
    class Meta:
        model = Venue
        fields = ['name', 'email', 'username', 'logo', 'description', 'address', 'capacity']

class ArtistForm(UserCreationForm):

    class Meta:
        model = Artist
        fields = ['name', 'username', 'email', 'logo', 'description', 'artistNumber']


class PerformanceForm(ModelForm):

    class Meta:
        model = Performance
        fields = ['name', 'description', 'date', 'public', 'description', 'venue', 'artist']


class VenueProfileForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'email', 'logo', 'description', 'address', 'capacity']

class ArtistProfileForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'email', 'logo', 'description', 'artistNumber']


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'description']


