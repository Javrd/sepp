from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import *
from .forms import ArtistForm
from mvp.models import Artist
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.template import loader
from datetime import datetime

from .forms import *
from .models import *


# Create your views here.
def lista_ofertas(request):
    offer_list = Offer.objects.all()
    context = {'offer_list': offer_list}
    return render(request, './lista_ofertas.html', context)


@permission_required('mvp.venue', login_url="/login")
def formulario_oferta(request):
    if request.method == 'POST':
        form = OfferForm(request.user, request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.venue = Venue.objects.get(id=request.user.id)
            offer.save()
            return HttpResponseRedirect('/lista_ofertas/')
    else:
        form = OfferForm(request.user)

    return render(request, './formulario_oferta.html', {'form': form})


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
            return redirect("/artinbar")
        else:
            formulario = AuthenticationForm()
            context = {'formulario': formulario}
            return render(request, 'login.html', context)
def login(request):
    if request.user.is_authenticated:
        return redirect("/artinbar")
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect("/artinbar")
        else:
            context = {'formulario': formulario}
            return render(request, 'login.html', context)

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


            url = request.GET.get('next', 'index')
            return redirect(url)

        context =  {'form':form}
        return render(request, 'artistForm.html', context)

def vista_artista(request, id_artista):
    artista = get_object_or_404(Artist, pk=id_artista)
    fotos = Photo.objects.filter(user=artista)
    multimedia = Media.objects.filter(artist=artista)

    context = {'artista': artista, 'fotos': fotos, 'multimedia': multimedia}
    return render(request, './vista_artista.html', context)


def vista_local(request, id_local):
    local = get_object_or_404(Venue, pk=id_local)
    fotos = Photo.objects.filter(user=local)
    geolocalizacion = Geolocation.objects.get(venue=local)

    context = {'local': local, 'fotos': fotos,
               'geolocalizacion': geolocalizacion}
    return render(request, './vista_local.html', context)


@login_required(login_url='/login')
def chat(request, user_id=None):

    principal = request.user
    if not user_id:
        contacts = (User.objects.filter(receivers__in=[principal]) | User.objects.filter(
            senders__in=[principal])).distinct()
        return render(request, 'contacts.html', {'contacts': contacts})

    else:
        contact = User.objects.get(id=user_id)

        if request.method == 'POST':
            form = request.POST
            msg = Message.objects.create(
                sender=principal, receiver=contact, timeStamp=datetime.now(), text=form['text'])
            data = {}
            data['date'] = msg.timeStamp.strftime("%d/%m/%Y %H:%m")
            data['text'] = msg.text
            return JsonResponse(data)

        messages = Message.objects.filter(receiver=principal, sender=contact) | Message.objects.filter(
            receiver=contact, sender=principal).order_by('timeStamp')
        last_contact_message = Message.objects.filter(
            receiver=principal, sender=contact).order_by('-timeStamp')
        if last_contact_message:
            last_contact_message = last_contact_message[0].id
        else:
            last_contact_message = -1
        return render(request, 'chat.html', {'messages': messages, 'contact': contact, 'last_contact_message': last_contact_message})


@login_required(login_url='/login')
def chat_sync(request, user_id=None):
    if request.method == 'POST':
        principal = request.user
        contact = User.objects.get(id=user_id)
        form = request.POST
        msg = Message.objects.filter(
            receiver=principal, sender=contact).order_by('-timeStamp')
        data = {}
        if msg:
            data['date'] = msg[0].timeStamp.strftime("%d/%m/%Y %H:%m")
            data['text'] = msg[0].text
            data['id'] = msg[0].id
        else:
            data['id'] = -1
        return JsonResponse(data)
