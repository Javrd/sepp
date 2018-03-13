from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import *


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
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'artistForm.html', {'form':form})