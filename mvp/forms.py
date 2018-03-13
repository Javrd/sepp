from django.contrib.auth.forms import *
from .models import Venue


class VenueForm(UserCreationForm):
    class Meta:
        model = Venue
        fields = ['geolocation', 'address', 'capacity']
        # fields = []
