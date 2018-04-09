from django.forms import ModelForm
from .models import *
from django.utils.translation import gettext_lazy as _

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

class VenueProfileForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'email', 'logo', 'description', 'address', 'capacity']

class ArtistProfileForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'email', 'logo', 'description', 'artistNumber']

class GeolocationForm(ModelForm):
    class Meta:
        model = Geolocation
        fields = ['latitude', 'longitude']