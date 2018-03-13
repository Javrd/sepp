from django.contrib.auth.forms import *
from .models import Venue, Artist


class VenueForm(UserCreationForm):
    class Meta:
        model = Venue
        fields = ['geolocation', 'address', 'capacity']
        # fields = []

class ArtistForm(UserCreationForm):

    class Meta:
        model = Artist
        fields = ['artistNumber']