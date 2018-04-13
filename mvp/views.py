from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.template import loader
from datetime import datetime
from django.forms import modelformset_factory

from .forms import *
from .models import *
import re


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

@permission_required('mvp.venue', login_url="/login")
def formulario_perfil_venue(request):
    venue = Venue.objects.get(id=request.user.id)
    geoloc = Geolocation.objects.get(venue=request.user.id)
    formSet = modelformset_factory(Photo, fields=('url','id',), )
    if request.method=='POST':
        venueForm = VenueProfileForm(request.POST, instance=venue, prefix='Ven')
        geoForm = GeolocationForm(request.POST, instance=geoloc,prefix='Geo')
        photoFormSet = formSet(request.POST, request.FILES, )

        if 'deletePhoto' in request.POST:
            idPhoto = request.POST.get('photoToDelete')
            if(idPhoto != None):
                photo = Photo.objects.get(id=idPhoto)
                if(photo.user == request.user):
                    photo.delete()
                    photoFormSet = formSet(queryset=Photo.objects.filter(user_id=request.user.id))

        elif ('edit' in request.POST and venueForm.is_valid() and geoForm.is_valid() 
            and photoFormSet.is_valid()):
            newVenue = venueForm.save(commit=False)
            newVenue.geolocation = geoForm.save(commit=False)
            newVenue.save()
            photos = photoFormSet.save(commit=False)
            for photo in photos:
                photo.user = request.user
                photo.save()
            return HttpResponseRedirect("/vista_local/"+str(request.user.id))
    else:
        
        venueForm = VenueProfileForm(instance=venue, prefix='Ven')
        geoForm = GeolocationForm(instance=geoloc, prefix='Geo')
        photoFormSet = formSet(queryset=Photo.objects.filter(user_id=request.user.id))

    context = {'venueForm': venueForm, 'geoForm': geoForm, 'photoFormSet': photoFormSet}
    return render(request, './formulario_perfil_local.html', context)

@permission_required('mvp.artist', login_url="/login")
def formulario_perfil_artist(request):
    artist = Artist.objects.get(id=request.user.id)
    formSetPhoto = modelformset_factory(Photo, fields=('url','id',), )
    formSetTag = modelformset_factory(Tag, fields=('name','id',), )
    formSetMedia = modelformset_factory(Media, fields=('url','id',), )    
    if request.method=='POST':
        artistForm = ArtistProfileForm(request.POST, instance=artist, prefix='Art')
        photoFormSet = formSetPhoto(request.POST, request.FILES, prefix='Photo', )
        tagFormSet = formSetTag(request.POST, request.FILES, prefix='Tag', )
        mediaFormSet = formSetMedia(request.POST, request.FILES, prefix='Media', )

        if 'deletePhoto' in request.POST:
            idPhoto = request.POST.get('photoToDelete')
            if(idPhoto != None):
                photo = Photo.objects.get(id=idPhoto)
                if(photo.user == request.user):
                    photo.delete()
                    photoFormSet = formSetPhoto(queryset=Photo.objects.filter(user_id=request.user.id), prefix='Photo')
        elif 'deleteTag' in request.POST:
            idTag = request.POST.get('tagToDelete')
            if(idTag != None):
                tag = Tag.objects.get(id=idTag)
                if(tag.artist_id == request.user.id):
                    tag.delete()
                    tagFormSet = formSetTag(queryset=Tag.objects.filter(artist_id=request.user.id), prefix='Tag')
        elif 'deleteMedia' in request.POST:
            idMedia = request.POST.get('mediaToDelete')
            if(idMedia != None):
                media = Media.objects.get(id=idMedia)
                if(media.artist_id == request.user.id):
                    media.delete()
                    mediaFormSet = formSetMedia(queryset=Media.objects.filter(artist_id=request.user.id), prefix='Media')
        elif ('edit' in request.POST and artistForm.is_valid() and photoFormSet.is_valid() 
            and tagFormSet.is_valid() and mediaFormSet.is_valid()):
            artistForm.save()
            photos = photoFormSet.save(commit=False)
            for photo in photos:
                photo.user = request.user
                photo.save()
            tags = tagFormSet.save(commit=False)
            for tag in tags:
                tag.artist_id = request.user.id
                tag.save()
            medias = mediaFormSet.save(commit=False)
            for media in medias:
                media.artist_id = request.user.id
                media.save()
            return HttpResponseRedirect("/vista_artista/"+str(request.user.id))
    else:
        
        artistForm = ArtistProfileForm(instance=artist, prefix='Art')
        photoFormSet = formSetPhoto(queryset=Photo.objects.filter(user_id=request.user.id), prefix='Photo')
        tagFormSet = formSetTag(queryset=Tag.objects.filter(artist_id=request.user.id), prefix='Tag')
        mediaFormSet = formSetMedia(queryset=Media.objects.filter(artist_id=request.user.id), prefix='Media')

    context = {'artistForm': artistForm, 'photoFormSet': photoFormSet, 'tagFormSet': tagFormSet,
        'mediaFormSet': mediaFormSet}
    return render(request, './formulario_perfil_artista.html', context)

def indexRedir(request):
    return redirect("/artinbar")


def index(request):
    template = loader.get_template('index.html')
    performance_list = Performance.objects.all()
    context = {'performance_list': performance_list}
    return HttpResponse(template.render(context, request))


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
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'login.html', context)


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
        messages = Message.objects.filter(
            receiver=principal, sender=contact).order_by('-timeStamp')
        data = []
        list = {'list': data}
        for i,msg in enumerate(messages):
            if (form["lastMessageId"] == msg.id):
                break
            data.append({})
            data[i]['date'] = msg.timeStamp.strftime("%d/%m/%Y %H:%m")
            data[i]['text'] = msg.text
            data[i]['id'] = msg.id
        data.reverse()
        return JsonResponse(list)
