from django.forms import ModelForm
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import *


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'description', 'offeredAmount', 'date']
        labels = {
            'name': _('Nombre'), 'description': _('Descripción'),
            'offeredAmount': _('Cantidad ofrecida'), 'date': _('Fecha'),
        }

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

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        #exclude = []
        fields = ['name', 'username', 'password', 'email', 'logo', 'description', 'artistNumber']




