from django.forms import ModelForm
from .models import *
from django.utils.translation import gettext_lazy as _

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'description', 'offeredAmount', 'date', 'venue']
        labels = {
            'name': _('Nombre'), 'description': _('Descripción'),
            'offeredAmount': _('Cantidad ofrecida'), 'date': _('Fecha'),
            'venue': _('Local'),
        }