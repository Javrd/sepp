from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import *
from .forms import ArtistForm
from mvp.models import Artist
from django.template import loader

def indexRedir(request):
    return redirect("/artinbar")


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def nuevoVenue(request):
    if request.method=='POST':
        formulario = VenueForm(request.POST, prefix='Ven')
        subformulario = GeolocationForm(request.POST, prefix='Geo')
        if formulario.is_valid() and subformulario.is_valid():
            newVenue = formulario.save()
            newGeo = subformulario.save()
            newVenue.geolocation = newGeo
            newVenue.save()
            return redirect("/artinbar")
    else:
        formulario = VenueForm(request.POST, prefix='Ven')
        subformulario = GeolocationForm(request.POST, prefix='Geo')
    context = {'formulario':formulario, 'subformulario':subformulario}
    return render(request, 'venueForm.html', context)

class registerArtistView(View):

    def get(self, request):
        form = ArtistForm()
        context = {'artist_form':form}

        return render(request, 'artistForm.html', context)

    def post(self, request):

        form = ArtistForm(request.POST)
        if form.is_valid():

            form_data = form.cleaned_data
            name = form_data.get("name")
            description = form_data.get("description")
            email = form_data.get("email")
            username = form_data.get("username")
            password = form_data.get("password")
            logo = form_data.get("logo")
            artist_number = form_data.get("artistNumber")
            artist = Artist.objects.create_user(name=name, description=description, logo=logo, username=username,email=email,password=password, artistNumber=artist_number)
            artist.save()

            url = request.GET.get('next', 'index')
            return redirect(url)

        context =  {'form':form}
        return render(request, 'artistForm.html', context)

