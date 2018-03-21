from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

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

def login(request):
    if request.user.is_authenticated:
        return redirect("/artinbar")
    if request.method=='POST':
        formulario=AuthenticationForm(data = request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect("/artinbar")
        else:
            context = {'formulario': formulario}
            return render(request, 'login.html', context)
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request,'login.html',context)

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

    context = {'local': local, 'fotos': fotos, 'geolocalizacion': geolocalizacion}
    return render(request, './vista_local.html', context)