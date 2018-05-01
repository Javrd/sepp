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

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['url', 'id']

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'id']

class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ['url', 'id']


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'description']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active & username:
            raise forms.ValidationError("Lo sentimos, esas credenciales son incorrectas. Por favor intentelo de nuevo.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


