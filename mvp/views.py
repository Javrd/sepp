from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import *
from .forms import ArtistForm
from mvp.models import Artist, Account


def nuevoVenue(request):
    if request.method=='POST':
        formulario = VenueForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('principal.views.inicio'))
    else:
        formulario = VenueForm(request.POST)
    context = {'formulario':formulario}
    return render(request, 'venueForm.html', context)

def newArtist(request):
    form = ArtistForm(request.POST or None)
    if form.is_valid():
        form_data = form.cleaned_data
        name = form_data.get("name")
        description = form_data.get("description")
        email = form_data.get("email")
        username = form_data.get("username")
        password = form_data.get("password")
        logo = form_data.get("logo")
        account = Account.objects.create(username=username,email=email,password=password)
        artist = Artist.objects.create(name=name, description=description, logo=logo, account=account)
        '''
        artist = Artist()
        artist.name = name
        artist.description = description
        account = Account()
        account.password = password
        account.username = username
        account.email = email
        artist.account = account
        artist.logo = logo
        artist.save()
        '''


    context =  {'form':form,}
    return render(request, 'artistForm.html', context)

