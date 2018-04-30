from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

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
from requests.auth import HTTPBasicAuth
import requests
import datetime
from django.contrib.auth.models import Permission
from django.forms import modelformset_factory
from .forms import *
from .models import *
import re
from django.utils.safestring import mark_safe
import json


# Create your views here.
def lista_ofertas(request):
    offer_list = Offer.objects.all().order_by('-date')
    context = {'offer_list': offer_list}
    return render(request, './lista_ofertas.html', context)


def lista_artistas(request):
    artist_list = Artist.objects.all()
    context = {'artist_list': artist_list}
    return render(request, './lista_artistas.html', context)


def lista_locales(request):
    venue_list = Venue.objects.all()
    context = {'venue_list': venue_list}
    return render(request, './lista_locales.html', context)


@permission_required('mvp.venue', login_url="/login")
def mis_ofertas(request):
    offer_list = Offer.objects.filter(
        venue_id=request.user.id).order_by('-date')
    context = {'offer_list': offer_list, 'propias': True, }
    return render(request, './lista_ofertas.html', context)


@permission_required('mvp.venue', login_url="/login")
def borrar_oferta(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    if(offer.venue.id == request.user.id):
        offer.delete()
    return redirect("/mis_ofertas")


@permission_required('mvp.venue', login_url="/login")
def formulario_oferta(request):
    if request.method == 'POST':
        form = OfferForm(request.user, request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.venue = Venue.objects.get(id=request.user.id)
            offer.save()
            return HttpResponseRedirect('/mis_ofertas/')
    else:
        form = OfferForm(request.user)

    return render(request, './formulario_oferta.html', {'form': form})


@permission_required('mvp.venue', login_url="/login")
def formulario_perfil_venue(request):
    venue = Venue.objects.get(id=request.user.id)
    geoloc = Geolocation.objects.get(venue=request.user.id)
    formSet = modelformset_factory(Photo, fields=('url', 'id',), )
    if request.method == 'POST':
        venueForm = VenueProfileForm(
            request.POST, instance=venue, prefix='Ven')
        geoForm = GeolocationForm(request.POST, instance=geoloc, prefix='Geo')
        photoFormSet = formSet(request.POST, request.FILES, )

        if 'deletePhoto' in request.POST:
            idPhoto = request.POST.get('photoToDelete')
            if(idPhoto != None):
                photo = Photo.objects.get(id=idPhoto)
                if(photo.user == request.user):
                    photo.delete()
                    photoFormSet = formSet(
                        queryset=Photo.objects.filter(user_id=request.user.id))

        elif ('edit' in request.POST and venueForm.is_valid() and geoForm.is_valid()
              and photoFormSet.is_valid()):
            newVenue = venueForm.save(commit=False)
            newVenue.geolocation = geoForm.save(commit=True)
            newVenue.save()
            photos = photoFormSet.save(commit=False)
            for photo in photos:
                photo.user = request.user
                photo.save()
            return HttpResponseRedirect("/vista_local/"+str(request.user.id))
    else:

        venueForm = VenueProfileForm(instance=venue, prefix='Ven')
        geoForm = GeolocationForm(instance=geoloc, prefix='Geo')
        photoFormSet = formSet(
            queryset=Photo.objects.filter(user_id=request.user.id))

    context = {'venueForm': venueForm,
               'geoForm': geoForm, 'photoFormSet': photoFormSet}
    return render(request, './formulario_perfil_local.html', context)


@permission_required('mvp.artist', login_url="/login")
def formulario_perfil_artist(request):
    artist = Artist.objects.get(id=request.user.id)
    formSetPhoto = modelformset_factory(Photo, fields=('url', 'id',), )
    formSetTag = modelformset_factory(Tag, fields=('name', 'id',), )
    formSetMedia = modelformset_factory(Media, fields=('url', 'id',), )
    if request.method == 'POST':
        artistForm = ArtistProfileForm(
            request.POST, instance=artist, prefix='Art')
        photoFormSet = formSetPhoto(
            request.POST, request.FILES, prefix='Photo', )
        tagFormSet = formSetTag(request.POST, request.FILES, prefix='Tag', )
        mediaFormSet = formSetMedia(
            request.POST, request.FILES, prefix='Media', )

        if 'deletePhoto' in request.POST:
            idPhoto = request.POST.get('photoToDelete')
            if(idPhoto != None):
                photo = Photo.objects.get(id=idPhoto)
                if(photo.user == request.user):
                    photo.delete()
                    photoFormSet = formSetPhoto(queryset=Photo.objects.filter(
                        user_id=request.user.id), prefix='Photo')
        elif 'deleteTag' in request.POST:
            idTag = request.POST.get('tagToDelete')
            if(idTag != None):
                tag = Tag.objects.get(id=idTag)
                if(tag.artist_id == request.user.id):
                    tag.delete()
                    tagFormSet = formSetTag(queryset=Tag.objects.filter(
                        artist_id=request.user.id), prefix='Tag')
        elif 'deleteMedia' in request.POST:
            idMedia = request.POST.get('mediaToDelete')
            if(idMedia != None):
                media = Media.objects.get(id=idMedia)
                if(media.artist_id == request.user.id):
                    media.delete()
                    mediaFormSet = formSetMedia(queryset=Media.objects.filter(
                        artist_id=request.user.id), prefix='Media')
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
        photoFormSet = formSetPhoto(queryset=Photo.objects.filter(
            user_id=request.user.id), prefix='Photo')
        tagFormSet = formSetTag(queryset=Tag.objects.filter(
            artist_id=request.user.id), prefix='Tag')
        mediaFormSet = formSetMedia(queryset=Media.objects.filter(
            artist_id=request.user.id), prefix='Media')

    context = {'artistForm': artistForm, 'photoFormSet': photoFormSet, 'tagFormSet': tagFormSet,
               'mediaFormSet': mediaFormSet}
    return render(request, './formulario_perfil_artista.html', context)


def indexRedir(request):
    return redirect("/")


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


class register_venue(View):

    def get(self, request):
        if request.user.is_authenticated:
            url = request.GET.get('next', 'index')
            return redirect(url)

        form = VenueForm()
        sub_form = GeolocationForm()

        context = {'venue_form': form, 'geo_form': sub_form}
        return render(request, 'register_venue.html', context)

    def post(self, request):
        form = VenueForm(request.POST)
        sub_form = GeolocationForm(request.POST)
        if form.is_valid() and sub_form.is_valid():
            new_venue = form.save()
            new_geo = sub_form.save()
            new_venue.geolocation = new_geo
            permission = Permission.objects.get(codename='venue')
            new_venue.user_permissions.add(permission)
            new_venue.save()
            url = request.GET.get('next', 'index')
            return redirect(url)

        context = {'venue_form': form, 'geo_form': sub_form}
        return render(request, 'register_venue.html', context)


class register_artist(View):

    def get(self, request):
        if request.user.is_authenticated:
            url = request.GET.get('next', 'index')
            return redirect(url)

        form = ArtistForm()
        context = {'artist_form': form}

        return render(request, 'register_artist.html', context)

    def post(self, request):

        form = ArtistForm(request.POST)
        if form.is_valid():

            new_artist = form.save()
            permission = Permission.objects.get(codename='artist')
            new_artist.user_permissions.add(permission)
            new_artist.save()

            url = request.GET.get('next', 'index')
            return redirect(url)

        context = {'artist_form': form}
        return render(request, 'register_artist.html', context)


def vista_artista(request, id_artista):
    artista = get_object_or_404(Artist, pk=id_artista)
    fotos = Photo.objects.filter(user=artista)
    media = Media.objects.filter(artist=artista)
    tags = Tag.objects.filter(artist=artista)
    multimedia = []
    for link in media:
        if '=' in link.url:
            multimedia.append(link.url.rpartition('=')[2])

    context = {'artista': artista, 'fotos': fotos, 'multimedia': multimedia,
               'tags': tags}
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
        
        principalIsVenue = Venue.objects.filter(pk=principal.id).exists()
        principalIsArtist = Artist.objects.filter(pk=principal.id).exists()
        contactIsVenue = Venue.objects.filter(pk=contact.id).exists()
        contactIsArtist = Artist.objects.filter(pk=contact.id).exists()

        if ((principalIsVenue and contactIsVenue) or (principalIsArtist and contactIsArtist)):
            return redirect("/chat")

        messages = Message.objects.filter(receiver=principal, sender=contact) | Message.objects.filter(
            receiver=contact, sender=principal).order_by('timeStamp')
        return render(request, './chat.html', {
            'messages': messages, 
            'contact': contact
    })


@login_required(login_url='/login')
def paypal(request, contact_id):
    offer_list = None
    try:
        contact = get_object_or_404(Venue, pk=contact_id)
        offer_list = Offer.objects.filter(
            venue_id=contact.id).order_by('-date')
    except:
        contact = get_object_or_404(Artist, pk=contact_id)

    principal = request.user

    if (offer_list is None):
        offer_list = Offer.objects.filter(
            venue_id=principal.id).order_by('-date')

    context = {'contact': contact, 'user': principal, 'offer_list': offer_list}
    return render(request, './paypal.html', context)


@login_required(login_url='/login')
def payment(request):

    form = request.POST
    payee = get_object_or_404(User, id=form['payee'])

    try:
        venue = Venue.objects.get(id=request.user.id).id
        artist = Artist.objects.get(id=payee.id).id
    except:
        artist = Artist.objects.get(id=request.user.id).id
        venue = Venue.objects.get(id=payee.id).id

    serializedPerformance = {
        'name': form['performanceName'],
        'description': form['performanceDes'],
        'date': form['performanceDate'],
        'public': form['performancePublic'],
        'artist': artist,
        'venue': venue
    }

    print('============ Performance info: ============')

    print('Name: '+serializedPerformance['name'])
    print('Description: '+serializedPerformance['description'])
    print('Date: '+serializedPerformance['date'])
    print('Public: '+serializedPerformance['public'])
    print('Artist: '+str(serializedPerformance['artist']))
    print('Venue: '+str(serializedPerformance['venue']))

    request.session['performance'] = serializedPerformance

    request.session['relaterOffer'] = form['relatedOffer']

    print('============ Requesting access token ============')
    payee = payee.email
    request.session['payee'] = payee
    amount = form['amount']
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    headers = {
        'accept': 'application/json',
        'Accept-Language': 'en_US'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    paypalResponse = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(
        'AYsiuq3v0vkhTIZrJA-pMAC-NJFG4LUG0AOphhoU52D0YHP1WiXpZ1ENIV_tcks6qutqVn99ZjR38lWg', 'ELZ-zqNT0hsVDUA5fjgguhlMIJTNjvu0A7y0_LqeBg_gChO9Ndjpy4gW-gpWbOZWnehZFCOlnco7Av_h'))
    json = paypalResponse.json()
    accessToken = json['access_token']

    print('Access Token obtained, expires in '+str(json['expires_in']))
    print('Access Token: '+accessToken)

    print('============ Creating payment ============')
    print('Payee: '+payee)
    print('Amount: '+amount)
    fee = float(amount)*0.05  # TODO: Fee?
    totalAmount = float(amount) + fee
    print('Fee: '+str(fee))
    print('Total amount: '+str(totalAmount))

    bearerToken = 'Bearer '+accessToken

    request.session['bearerToken'] = bearerToken

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearerToken
    }

    amount1 = {
        'total': str(totalAmount),
        'currency': 'EUR',
        'details': {
            'subtotal': str(amount),
            'handling_fee': str(fee)
        }
    }

    transaction1 = {
        'amount': amount1,
        'description': 'Pago a Art in Bar',
        'payment_options': {
            'allowed_payment_method': 'IMMEDIATE_PAY'
        }
    }

    transactions = [transaction1]

    data = {
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'transactions': transactions,
        'note_to_payer': 'Puedes contactar con nosotros para cualquier duda en pagosartinbar@gmail.com',
        'redirect_urls': {
            'return_url': 'http://localhost:8000/artinbar',
            'cancel_url': 'http://localhost:8000/artinbar'
        }
    }

    saleUrl = 'https://api.sandbox.paypal.com/v1/payments/payment'

    payment = requests.post(saleUrl, headers=headers, json=data).json()

    if (payment['id'] is not None):
        print('Payment id: '+payment['id'])
        print('============ Payment created succesfully ============')

    return JsonResponse(payment)


def executePayment(request):
    paymentId = request.POST.get('paymentID')
    payerId = request.POST.get('payerID')
    #print('============ Requesting access token ============')

    #url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    # headers = {
    #    'accept': 'application/json',
    #    'Accept-Language': 'en_US'
    #}
    # data = {
    #    'grant_type': 'client_credentials'
    #}
    # paypalResponse = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(
    #    'AYsiuq3v0vkhTIZrJA-pMAC-NJFG4LUG0AOphhoU52D0YHP1WiXpZ1ENIV_tcks6qutqVn99ZjR38lWg', 'ELZ-zqNT0hsVDUA5fjgguhlMIJTNjvu0A7y0_LqeBg_gChO9Ndjpy4gW-gpWbOZWnehZFCOlnco7Av_h'))
    #json = paypalResponse.json()
    #accessToken = json['access_token']

    #print('Access Token obtained, expires in '+str(json['expires_in']))
    #print('Access Token: '+accessToken)

    print('============ Building payment execution request ============')
    print('Payment ID: '+paymentId)
    print('Payer ID: '+payerId)

    executeUri = 'https://api.sandbox.paypal.com/v1/payments/payment/'+paymentId+'/execute/'

    bearerToken = request.session['bearerToken']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearerToken
    }

    data = {
        'payer_id': payerId
    }

    payment = requests.post(executeUri, headers=headers, json=data).json()

    if (payment['state'] == 'approved'):
        request.session['payment'] = payment
        return payout(request)
    else:
        return HttpResponse('ERROR')


def payout(request):
    payment = request.session['payment']
    bearerToken = request.session['bearerToken']
    payee = request.session['payee']
    amount = payment['transactions'][0]['amount']['details']['subtotal']
    batchId = payment['id']
    emailMessage = '¡Felicidades! Acabas de recibir un pago de '+amount + \
        '€ a través de Art in Bar.'  # TODO: Currarse un poco el mensaje, poner datos

    print('============ Creating payout ============')
    print('Payee: '+payee)
    print('Amount: '+amount)
    print('Sender batch ID: '+batchId)

    payoutsURI = 'https://api.sandbox.paypal.com/v1/payments/payouts'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearerToken
    }

    data = {
        'sender_batch_header': {
            'sender_batch_id': batchId,
            'email_subject': 'Pago de Art in Bar',
            'email_message': emailMessage
        },
        'items': [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": amount,
                    "currency": "EUR"
                },
                "note": "¡Gracias por usar Art in Bar!",
                "sender_item_id": batchId,
                "receiver": payee
            }
        ]
    }

    payout = requests.post(payoutsURI, headers=headers, json=data).json()

    if (payout['batch_header']['batch_status'] == 'PENDING'):
        print('============ Payout successfully processed ============')

    serializedPerformance = request.session['performance']
    performance = Performance()

    performance.name = serializedPerformance['name']
    performance.description = serializedPerformance['description']
    performance.date = serializedPerformance['date']
    performance.public = True if serializedPerformance['public'] is 'on' else False
    performance.artist = Artist.objects.get(id=serializedPerformance['artist'])
    performance.venue = Venue.objects.get(id=serializedPerformance['venue'])

    performance.save()
    print('============ Performance saved ============')

    paymentObject = Payment()
    paymentObject.amount = payment['transactions'][0]['amount']['total']
    paymentObject.user = request.user
    paymentObject.performance = performance
    paymentObject.date = datetime.datetime.now()
    paymentObject.paypalId = payment['id']

    paymentObject.save()
    print('============ Payment saved ============')

    offerId = request.session['relaterOffer']
    if (offerId != 0):
        offer = Offer.objects.get(id=offerId)
        offer.delete()

    return HttpResponse('OK')


@login_required(login_url='/login')
def paymentConfirmation(request):
    payment = request.session['payment']
    return render(request, './paypalConfirm.html', {'payment': payment})




class formulario_feedback(View):

    def get(self, request):

        form = FeedbackForm()
        context = {'feedback_form': form}

        return render(request, 'feedback.html', context)

    def post(self, request):

        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()

            url = request.GET.get('next', 'index')
            return redirect(url)

        context = {'feedback_form': form}
        return render(request, 'feedback.html', context)


def vote(request):
    return redirect('https://docs.google.com/forms/d/e/1FAIpQLSfqL7wY8eZ4NLD_Bd9Z_jbg4UOM6ceBIi54mV6ObW7irG711w/viewform?usp=sf_link')


def termsAndConditions(request):

    return render(request, './T&C.html')

