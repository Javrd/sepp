from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import *
from .forms import ArtistForm
from mvp.models import Artist, Account
from django.template import loader



def indexRedir(request):
    return redirect("/artinbar")


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
            return HttpResponseRedirect(reverse('principal.views.inicio'))
    else:
        formulario = VenueForm(request.POST, prefix='Ven')
        subformulario = GeolocationForm(request.POST, prefix='Geo')
    context = {'formulario':formulario, 'subformulario':subformulario}
    return render(request, 'venueForm.html', context)

def artistForm(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST or None)
        if form.is_valid():

            form_data = form.cleaned_data
            name = form_data.get("name")
            description = form_data.get("description")
            email = form_data.get("email")
            username = form_data.get("username")
            password = form_data.get("password")
            logo = form_data.get("logo")
            artistNumber = form_data.get("artistNumber")
            account = Account.objects.create(username=username,email=email,password=password)
            artist = Artist.objects.create(name=name, description=description, logo=logo, account=account, artistNumber=artistNumber)

            return HttpResponseRedirect('/index/')

    else:
        form = ArtistForm()


    context =  {'form':form,}
    return render(request, 'artistForm.html', context)

