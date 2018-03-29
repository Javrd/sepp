from django.forms import ModelForm
from .models import Offer
from django.utils.translation import gettext_lazy as _


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'description', 'offeredAmount', 'date']
        labels = {
            'name': _('Nombre'), 'description': _('Descripción'),
            'offeredAmount': _('Cantidad ofrecida'), 'date': _('Fecha'),
        }

class GeolocationForm(ModelForm):

    class Meta:
        model = Geolocation
        fields = ['latitude', 'longitude']


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        #exclude = []
        fields = ['name', 'username', 'password', 'email', 'logo', 'description', 'artistNumber']


        
    def __init__(self, user, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.venue = user
